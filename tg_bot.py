import random

from environs import Env
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler

from buttons import reply_markup
from settings_db import questions_redis, users_redis, points_redis

NEW_QUESTION, ANSWER, REFUSAL = range(3)


def start_callback(update, _):
    """Кнопка /start."""
    points_redis.set(f'{update.message.chat.id}', '0')
    update.message.reply_text("Привет! Я бот для викторин! Для начала игры нажми кнопку «Новый вопрос»!",
                              reply_markup=reply_markup)
    return NEW_QUESTION


def handle_new_question_request(update, _):
    question = random.choice(list(questions.keys()))
    users_redis.set(f'{update.message.chat.id}', f'{question}')
    update.message.reply_text(f'{question}',
                              reply_markup=reply_markup, parse_mode='HTML')
    return ANSWER


def handle_solution_attempt(update, _):
    correct_anwser = questions[users_redis.get(f"{update.message.chat.id}")]
    if update.message.text == correct_anwser:
        number_points = int(points_redis.get(update.message.chat.id)) + 1
        points_redis.set(f'{update.message.chat.id}', f'{number_points}')
        update.message.reply_text("Правильно! Поздравляю! Для следующего вопроса нажми «Новый вопрос».")
        return NEW_QUESTION
    else:
        update.message.reply_text("Неправильно… Попробуешь ещё раз?")
        return ANSWER


def handle_message_correct_answer(update, context):
    correct_anwser = questions[users_redis.get(f"{update.message.chat.id}")]
    context.bot.send_message(update.effective_chat.id,
                             f'<b>Правильный ответ:</b>\n{correct_anwser}',
                             reply_markup=reply_markup, parse_mode='HTML')
    handle_new_question_request(update, context)
    return ANSWER


def handle_number_points(update, context):
    context.bot.send_message(update.effective_chat.id,
                             f'<b>Количество правильных ответов:</b>\n{points_redis.get(update.message.chat.id)}',
                             parse_mode='HTML')


if __name__ == "__main__":
    env = Env()
    env.read_env()

    updater = Updater(env.str("TELEGRAM_BOT_TOKEN"))

    questions = questions_redis.hgetall("quiz")

    conv_handler = ConversationHandler(
        entry_points=[
            CommandHandler('start', start_callback),
            MessageHandler(Filters.text('Мой счет'), handle_number_points)
        ],
        states={
            NEW_QUESTION: [
                MessageHandler(Filters.text('Новый вопрос'), handle_new_question_request),
                MessageHandler(Filters.text('Мой счёт'), handle_number_points)],
            ANSWER: [
                MessageHandler(Filters.text('Мой счёт'), handle_number_points),
                MessageHandler(Filters.text('Сдаться'), handle_message_correct_answer),
                MessageHandler(Filters.text, handle_solution_attempt),
            ]
        },
        fallbacks=[]
    )

    dispatcher = updater.dispatcher
    dispatcher.add_handler(conv_handler)

    updater.start_polling()
