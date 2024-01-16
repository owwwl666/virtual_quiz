import logging
import random

import telegram
import vk_api as vk
from environs import Env
from vk_api.keyboard import VkKeyboard
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id

from logger_bot import TelegramLogsHandler
from settings_db import questions_redis, users_redis, points_redis


def add_keyboard():
    """Добавляет кнопки боту."""

    keyboard = VkKeyboard()

    keyboard.add_button("Новый вопрос")
    keyboard.add_button("Сдаться")

    keyboard.add_line()
    keyboard.add_button("Мой счёт")

    return keyboard.get_keyboard()


def start(event):
    """Запускает новую викторину.

    Обнуляет количество правильных ответов."""
    points_redis.set(f"{event.user_id}", "0")
    vk_api.messages.send(
        user_id=event.user_id,
        random_id=get_random_id(),
        keyboard=add_keyboard(),
        message="Для начала игры нажми кнопку «Новый вопрос»!",
    )


def get_random_question(event, questions):
    """Возвращает рандомный вопрос и выдает его пользователю."""
    question = random.choice(list(questions.keys()))
    users_redis.set(f"{event.user_id}", f"{question}")
    return vk_api.messages.send(
        user_id=event.user_id,
        random_id=get_random_id(),
        keyboard=add_keyboard(),
        message=f"{question}",
    )


def check_correct_answer(event):
    """Проверяет данный пользователем ответ на правильность."""
    correct_anwser = questions[users_redis.get(f"{event.user_id}")]
    if event.text == correct_anwser:
        number_points = int(points_redis.get(event.user_id)) + 1
        points_redis.set(f"{event.user_id}", f"{number_points}")
        return vk_api.messages.send(
            user_id=event.user_id,
            random_id=get_random_id(),
            keyboard=add_keyboard(),
            message="Правильно! Поздравляю! Для следующего вопроса нажми «Новый вопрос».",
        )
    return vk_api.messages.send(
        user_id=event.user_id,
        random_id=get_random_id(),
        keyboard=add_keyboard(),
        message="Неправильно… Попробуешь ещё раз?",
    )


def report_correct_answer(event, vk_api, questions):
    """Сообщает пользователю правильный ответ при нажатии на кнопку 'Сдаться'."""
    correct_anwser = questions[users_redis.get(f"{event.user_id}")]
    return vk_api.messages.send(
        user_id=event.user_id,
        random_id=get_random_id(),
        keyboard=add_keyboard(),
        message=f"Правильный ответ: {correct_anwser}\nДля того, чтобы продолжить, нажмите «Новый вопрос».",
    )


def get_number_points(event):
    """Выдает количетсво правильных ответов в текущей викторине."""
    points = points_redis.get(event.user_id)
    return vk_api.messages.send(
        user_id=event.user_id,
        random_id=get_random_id(),
        keyboard=add_keyboard(),
        message=f"Количество правильных ответов:\n{points}",
    )


if __name__ == "__main__":
    env = Env()
    env.read_env()

    logger = logging.getLogger("logger")
    log_bot = telegram.Bot(token=env.str("LOGGER_BOT_TOKEN"))

    logging.basicConfig(format="%(levelname)s::%(message)s", level=logging.ERROR)
    logger.addHandler(TelegramLogsHandler(bot=log_bot, chat_id=env.str("CHAT_ID")))

    vk_session = vk.VkApi(token=env.str("VK_BOT_TOKEN"))
    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)

    questions = questions_redis.hgetall("quiz")

    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            try:
                if event.text == "Начать":
                    start(event)

                elif event.text == "Новый вопрос":
                    get_random_question(event, questions)

                elif event.text == "Сдаться":
                    report_correct_answer(event, vk_api, questions)

                elif event.text == "Мой счёт":
                    get_number_points(event)

                else:
                    check_correct_answer(event)
            except Exception as err:
                logger.error(err, exc_info=True)
