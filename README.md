### Support bot

The program answer for users messages in [Telegram](https://telegram.org/) and [VK](https://vk.com/) according [DialogFlow](https://dialogflow.cloud.google.com/) intents.

Dialogflow is a Google-owned developer of human–computer interaction technologies based on natural language conversations.

![](https://github.com/NecrOctopuS/support_bot/blob/master/Bot.gif)
 
### How to install

Then you need to deploy this project to [Heroku](https://heroku.com/)

On [Heroku](https://heroku.com/) you need create the app, and connect it to this project.

In Settings -> Config Vars you need add next variables

```text
TELEGRAM_TOKEN='4645646:asd4a6dadawee4da6d4s'
TELEGRAM_ID='123456789'
PROJECT_ID='devman-support-bot-269007'
VK_TOKEN='7fe50745b17ebda65a722b03b884419409747760d218b360b4efdd83c6b32b3fca86f05a4f1d52029fe81'
GOOGLE_APPLICATION_CREDENTIALS='google-credentials.json'
GOOGLE_CREDENTIALS='your Google credintials'
FILENAME='questions.json'
```
`DEVMAN_TOKEN` can be take it from [Devman](https://dvmn.org/api/docs/).

`TELEGRAM_TOKEN` can be take it from [BotFather](https://telegram.me/BotFather) by type `/start`
`/newbot`.

`TELEGRAM_ID` can be take it from [userinfobot](https://telegram.me/userinfobot) by type `/start`.

`PROJECT_ID` it is your Project ID from [DialogFlow](https://dialogflow.cloud.google.com/).

`VK_TOKEN` can be taken from settings API for your group in [VK](https://vk.com/).

`GOOGLE_APPLICATION_CREDENTIALS` can be taken from [Google](https://cloud.google.com/docs/authentication/getting-started)

`FILENAME` it is yours filename for question intents, that you wont to upload to [DialogFlow](https://dialogflow.cloud.google.com/).

After that in Resources you need turn on bot.

Also you need to run command
```
heroku buildpacks:add https://github.com/gerywahyunugraha/heroku-google-application-credentials-buildpack
```

### How to run

In telegram or vk you need to write to your bot any message.
Bot will answer you.

### How to add intents

In file `FILENAME` your questions need to be in this structure:
```json
{
    "Устройство на работу": {
        "questions": [
            "Как устроиться к вам на работу?",
            "Как устроиться к вам?",
            "Как работать у вас?",
            "Хочу работать у вас",
            "Возможно-ли устроиться к вам?",
            "Можно-ли мне поработать у вас?",
            "Хочу работать редактором у вас"
        ],
        "answer": "Если вы хотите устроиться к нам, напишите на почту game-of-verbs@gmail.com мини-эссе о себе и прикрепите ваше портфолио."
    },
```
You need to run script
```commandline
python dialog_flow.py
```

### Objective of the project

The code is written for educational purposes on the online course for web developers [dvmn.org](https://dvmn.org/).