from dotenv import load_dotenv
import os
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
import random
import logging
import telegram
from bot_tools import TelegramLogsHandler, detect_intent_texts_without_fallback

load_dotenv()
TELEGRAM_TOKEN = os.environ['TELEGRAM_TOKEN']
VK_TOKEN = os.environ['VK_TOKEN']
PROJECT_ID = os.environ['PROJECT_ID']
LANGUAGE_CODE = 'ru'
GOOGLE_APPLICATION_CREDENTIALS = os.environ['GOOGLE_APPLICATION_CREDENTIALS']
TELEGRAM_ID = os.environ['TELEGRAM_ID']

logger = logging.getLogger('telegram_logger')


def echo(event, vk_api):
    text = detect_intent_texts_without_fallback(PROJECT_ID, event.user_id, event.text, LANGUAGE_CODE)
    if text:
        vk_api.messages.send(
            user_id=event.user_id,
            message=text,
            random_id=random.randint(1, 1000)
        )


if __name__ == "__main__":
    tg_bot = telegram.Bot(token=TELEGRAM_TOKEN)
    logger.setLevel(logging.WARNING)
    logger.addHandler(TelegramLogsHandler(tg_bot, TELEGRAM_ID))
    vk_session = vk_api.VkApi(token=VK_TOKEN)
    vk_api = vk_session.get_api()
    try:
        longpoll = VkLongPoll(vk_session)
    except Exception as e:
        logger.exception(e)
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            try:
                echo(event, vk_api)
            except Exception as e:
                logger.exception(e)
