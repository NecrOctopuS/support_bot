from dotenv import load_dotenv
import os
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
import random
import logging
import telegram
import dialogflow_v2 as dialogflow

load_dotenv()
TELEGRAM_TOKEN = os.environ['TELEGRAM_TOKEN']
VK_TOKEN = os.environ['VK_TOKEN']
PROJECT_ID = os.environ['PROJECT_ID']
LANGUAGE_CODE = 'ru'
GOOGLE_APPLICATION_CREDENTIALS = os.environ['GOOGLE_APPLICATION_CREDENTIALS']
TELEGRAM_ID = os.environ['TELEGRAM_ID']


class TelegramLogsHandler(logging.Handler):

    def __init__(self, tg_bot, chat_id):
        super().__init__()
        self.chat_id = chat_id
        self.tg_bot = tg_bot

    def emit(self, record):
        log_entry = self.format(record)
        self.tg_bot.send_message(chat_id=self.chat_id, text=log_entry)


tg_bot = telegram.Bot(token=TELEGRAM_TOKEN)
logger = logging.getLogger('telegram_logger')
logger.setLevel(logging.WARNING)
logger.addHandler(TelegramLogsHandler(tg_bot, TELEGRAM_ID))


def detect_intent_texts(project_id, session_id, text, language_code):
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)
    text_input = dialogflow.types.TextInput(text=text, language_code=language_code)
    query_input = dialogflow.types.QueryInput(text=text_input)
    response = session_client.detect_intent(session=session, query_input=query_input)
    if not response.query_result.intent.is_fallback:
        return response.query_result.fulfillment_text
    else:
        return None


def echo(event, vk_api):
    text = detect_intent_texts(PROJECT_ID, event.user_id, event.text, LANGUAGE_CODE)
    if text:
        vk_api.messages.send(
            user_id=event.user_id,
            message=text,
            random_id=random.randint(1, 1000)
        )


if __name__ == "__main__":
    vk_session = vk_api.VkApi(token=VK_TOKEN)
    vk_api = vk_session.get_api()
    try:
        longpoll = VkLongPoll(vk_session)
    except Exception as e:
        logger.critical(e, exc_info=True)
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            try:
                echo(event, vk_api)
            except Exception as e:
                logger.warning(e, exc_info=True)
