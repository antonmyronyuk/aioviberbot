from aioviberbot import Api, BotConfiguration
from aioviberbot.api.messages.text_message import TextMessage

TOKEN = '4e2a50206527dd1a-b159133a6c7aa3db-ca8c1524c10d9ee8'

viber = Api(BotConfiguration(
    name='Test phish bot',
    avatar='https://viber.com/avatar.jpg',
    auth_token=TOKEN,
))

async def run():
    print('here')
    print(await viber.get_account_info())
    try:
        print(await viber.get_user_details('wtNpzB6pfOO7vhAf0GGbgA=='))
    except Exception as e:
        print(e)

    try:
        await viber.send_messages('wtNpzB6pfOO7vhAf0GGbgA==', TextMessage(text='test msg 2'))
    except Exception as e:
        print(e)

print('here')
import asyncio
asyncio.run(run())
