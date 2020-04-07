import dialogflow_v2
from dotenv import load_dotenv
import os
import json

load_dotenv()
PROJECT_ID = os.getenv('PROJECT_ID')
GOOGLE_APPLICATION_CREDENTIALS = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
FILENAME = os.getenv('FILENAME')


def create_intents_from_file(FILENAME):
    with open(FILENAME, "r", encoding='utf-8') as my_file:
        question_dict = json.load(my_file)
    intents = []
    for theme in question_dict.keys():
        answer = question_dict[theme]['answer']
        questions = question_dict[theme]['questions']
        training_phrases = []
        for question in questions:
            training_phrase = {
                "parts": [{"text": question}]
            }
            training_phrases.append(training_phrase)
        intent = {
            "display_name": theme,
            "messages": [{
                "text":
                    {"text": [answer]}
            }],
            "training_phrases": training_phrases
        }
        intents.append(intent)
    return intents


def main():
    client = dialogflow_v2.IntentsClient()
    parent = client.project_agent_path(PROJECT_ID)
    intents = create_intents_from_file(FILENAME)
    for intent in intents:
        response = client.create_intent(parent, intent)


if __name__ == '__main__':
    main()
