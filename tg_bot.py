import json
import random

import redis
from environs import Env
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

from buttons import reply_markup


def start_callback(update, _):
    """Кнопка /start."""
    update.message.reply_text("Привет! Я бот для викторин!", reply_markup=reply_markup)


def reply_message(update, _):
    if update.message.text == 'Новый вопрос':
        questions = list(r.hgetall("quiz").keys())
        question = random.choice(questions)
        update.message.reply_text(question, reply_markup=reply_markup, parse_mode='HTML')


if __name__ == "__main__":
    r = redis.Redis(host='localhost', port=6379, decode_responses=True, db=0)

    env = Env()
    env.read_env()

    updater = Updater(env.str("TELEGRAM_BOT_TOKEN"))

    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler('start', start_callback))
    dispatcher.add_handler(MessageHandler(Filters.all, reply_message))

    updater.start_polling()
