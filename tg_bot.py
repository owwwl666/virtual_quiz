from environs import Env
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler


def start_callback(update, _):
    """Кнопка /start."""
    update.message.reply_text("Здравствуйте!")


def replie_to_message(update, context):
    update.message.reply_text(update.message.text)


if __name__ == "__main__":
    env = Env()
    env.read_env()

    updater = Updater(env.str("TELEGRAM_BOT_TOKEN"))

    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler('start', start_callback))
    dispatcher.add_handler(MessageHandler(Filters.text, replie_to_message))


    updater.start_polling()
