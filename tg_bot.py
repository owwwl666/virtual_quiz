import random

import redis
from environs import Env
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

from buttons import reply_markup


def start_callback(update, _):
    """Кнопка /start."""
    update.message.reply_text("Привет! Я бот для викторин!", reply_markup=reply_markup)


def reply_message(update, _):
    questions = r.hgetall("quiz")
    if update.message.text == 'Новый вопрос':
        question = random.choice(list(questions.keys()))
        r.set(f'{update.message.chat.id}', f'{question}')
        update.message.reply_text(f'{question}\n{questions[r.get(f"{update.message.chat.id}")]}',
                                  reply_markup=reply_markup, parse_mode='HTML')
    elif update.message.text == questions[r.get(f"{update.message.chat.id}")]:
        update.message.reply_text("Правильно! Поздравляю! Для следующего вопроса нажми «Новый вопрос».")
    else:
        update.message.reply_text("Неправильно… Попробуешь ещё раз?")


if __name__ == "__main__":
    r = redis.Redis(host='localhost', port=6379, decode_responses=True, db=0)

    env = Env()
    env.read_env()

    updater = Updater(env.str("TELEGRAM_BOT_TOKEN"))

    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler('start', start_callback))
    dispatcher.add_handler(MessageHandler(Filters.all, reply_message))

    updater.start_polling()
