from viberbot import Api, BotConfiguration
from viberbot.api.messages.text_message import TextMessage

TOKEN = '4e2a50206527dd1a-b159133a6c7aa3db-ca8c1524c10d9ee8'

viber = Api(BotConfiguration(
    name='Test phish bot',
    avatar='https://viber.com/avatar.jpg',
    auth_token=TOKEN,
))

async def run():
    print(await viber.get_user_details('wtNpzB6pfOO7vhAf0GGbgA=='))
    await viber.send_messages('wtNpzB6pfOO7vhAf0GGbgA==', TextMessage(text='test msg'))

import asyncio
asyncio.run(run())
