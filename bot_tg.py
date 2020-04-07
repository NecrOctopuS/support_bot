from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from dotenv import load_dotenv
import logging
import os
import telegram

from bot_tools import TelegramLogsHandler, detect_intent_texts

load_dotenv()
TELEGRAM_TOKEN = os.environ['TELEGRAM_TOKEN']
PROJECT_ID = os.environ['PROJECT_ID']
GOOGLE_APPLICATION_CREDENTIALS = os.environ['GOOGLE_APPLICATION_CREDENTIALS']
TELEGRAM_ID = os.environ['TELEGRAM_ID']
LANGUAGE_CODE = 'ru'

tg_bot = telegram.Bot(token=TELEGRAM_TOKEN)
logger = logging.getLogger('telegram_logger')
logger.setLevel(logging.WARNING)
logger.addHandler(TelegramLogsHandler(tg_bot, TELEGRAM_ID))


def start(bot, update):
    update.message.reply_text('Hi!')


def help(bot, update):
    update.message.reply_text('Help!')


def echo(bot, update):
    text = detect_intent_texts(PROJECT_ID, update.message.from_user['id'], update.message.text, LANGUAGE_CODE)
    update.message.reply_text(text)


def error(bot, update, error):
    logger.warning('Update "%s" caused error "%s"', update, error)


def main():
    updater = Updater(TELEGRAM_TOKEN)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(MessageHandler(Filters.text, echo))
    dp.add_error_handler(error)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
