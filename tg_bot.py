import logging
import random
from enum import Enum

import telegram
from environs import Env
from telegram import ReplyKeyboardMarkup
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
)

from logger_bot import TelegramLogsHandler
from settings_db import questions_redis, users_redis, points_redis


class Quiz(Enum):
    NEW_QUESTION = 1
    ANSWER = 2


def start(update, _):
    """Кнопка /start - запуск викторины."""
    points_redis.set(f"{update.message.chat.id}", "0")
    update.message.reply_text(
        "Привет! Я бот для викторин! Для начала игры нажми кнопку «Новый вопрос»!",
        reply_markup=reply_markup,
    )
    return Quiz.NEW_QUESTION


def handle_new_question_request(update, _):
    """Задает пользователю новый рандомный вопрос."""
    question = random.choice(list(questions.keys()))
    users_redis.set(f"{update.message.chat.id}", f"{question}")
    update.message.reply_text(
        f"{question}", reply_markup=reply_markup, parse_mode="HTML"
    )
    return Quiz.ANSWER


def handle_solution_attempt(update, _):
    """Проверяет правильность ответа на вопрос."""
    correct_anwser = questions[users_redis.get(f"{update.message.chat.id}")]
    if update.message.text == correct_anwser:
        number_points = int(points_redis.get(update.message.chat.id)) + 1
        points_redis.set(f"{update.message.chat.id}", f"{number_points}")
        update.message.reply_text(
            "Правильно! Поздравляю! Для следующего вопроса нажми «Новый вопрос»."
        )
        return Quiz.NEW_QUESTION
    update.message.reply_text("Неправильно… Попробуешь ещё раз?")
    return Quiz.ANSWER


def handle_message_correct_answer(update, context):
    """Сообщает пользователю правильный ответ, если он сдается."""
    correct_anwser = questions[users_redis.get(f"{update.message.chat.id}")]
    context.bot.send_message(
        update.effective_chat.id,
        f"<b>Правильный ответ:</b>\n{correct_anwser}\nДля того, чтобы продолжить, нажмите «Новый вопрос».",
        reply_markup=reply_markup,
        parse_mode="HTML",
    )
    return Quiz.NEW_QUESTION


def handle_number_points(update, context):
    """Сообщает пользователю о количестве правильно данных ответов на вопросы."""
    context.bot.send_message(
        update.effective_chat.id,
        f"<b>Количество правильных ответов:</b>\n{points_redis.get(update.message.chat.id)}",
        parse_mode="HTML",
    )


def cancel(update, _):
    """Кнопка /cancel - завершение викторины и выход из нее."""
    number_points = points_redis.get(update.message.chat.id)
    update.message.reply_text(
        f"Спасибо, за участие в Викторине!\nВаше количество правильных ответов: <b>{number_points}</b>",
        parse_mode="HTML",
    )
    return ConversationHandler.END


def handle_errors(update, context):
    """Обработчик исключений."""
    logger.error(Exception, exc_info=True)


if __name__ == "__main__":
    env = Env()
    env.read_env()

    logger = logging.getLogger("logger")
    log_bot = telegram.Bot(token=env.str("LOGGER_BOT_TOKEN"))

    logging.basicConfig(format="%(levelname)s::%(message)s", level=logging.ERROR)
    logger.addHandler(TelegramLogsHandler(bot=log_bot, chat_id=env.str("CHAT_ID")))

    reply_markup = ReplyKeyboardMarkup([["Новый вопрос", "Сдаться"], ["Мой счёт"]])

    updater = Updater(env.str("TELEGRAM_BOT_TOKEN"))

    questions = questions_redis.hgetall("quiz")

    conv_handler = ConversationHandler(
        entry_points=[
            CommandHandler("start", start),
            MessageHandler(Filters.text("Мой счет"), handle_number_points),
        ],
        states={
            Quiz.NEW_QUESTION: [
                CommandHandler("cancel", cancel),
                MessageHandler(
                    Filters.text("Новый вопрос"), handle_new_question_request
                ),
                MessageHandler(Filters.text("Мой счёт"), handle_number_points),
            ],
            Quiz.ANSWER: [
                CommandHandler("cancel", cancel),
                MessageHandler(Filters.text("Мой счёт"), handle_number_points),
                MessageHandler(Filters.text("Сдаться"), handle_message_correct_answer),
                MessageHandler(Filters.text, handle_solution_attempt),
            ],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    dispatcher = updater.dispatcher
    dispatcher.add_handler(conv_handler)
    dispatcher.add_error_handler(handle_errors)

    updater.start_polling()
