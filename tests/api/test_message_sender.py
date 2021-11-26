import logging
from unittest.mock import Mock

import pytest

from aioviberbot.api.bot_configuration import BotConfiguration
from aioviberbot.api.consts import BOT_API_ENDPOINT
from aioviberbot.api.message_sender import MessageSender
from aioviberbot.api.messages import TextMessage

logger = logging.getLogger('super-logger')
VIBER_BOT_CONFIGURATION = BotConfiguration(
    auth_token='auth-token-sample',
    name='testbot',
    avatar='https://avatars.com/avatar.jpg',
)


async def test_send_message_sanity():
    to = '012345A='
    text = 'hi!'
    message_token = 'a token'
    chat_id = 'my chat id sample'

    async def post_request(endpoint, payload):
        assert endpoint == BOT_API_ENDPOINT.SEND_MESSAGE
        assert payload['receiver'] == to
        assert payload['sender']['name'] == VIBER_BOT_CONFIGURATION.name
        assert payload['sender']['avatar'] == VIBER_BOT_CONFIGURATION.avatar
        assert payload['text'] == text
        assert payload['chat_id'] == chat_id
        return dict(status=0, message_token=message_token)

    request_sender = Mock()
    request_sender.post_request = post_request

    text_message = TextMessage(text=text)

    message_sender = MessageSender(logger, request_sender)
    token = await message_sender.send_message(
        to, VIBER_BOT_CONFIGURATION.name, VIBER_BOT_CONFIGURATION.avatar, text_message, chat_id)
    assert token == message_token


async def test_post_to_public_account_sanity():
    sender = '012345A='
    text = 'hi!'
    message_token = 'a token'

    async def post_request(endpoint, payload):
        assert endpoint == BOT_API_ENDPOINT.POST
        assert payload['from'] == sender
        assert payload['sender']['name'] == VIBER_BOT_CONFIGURATION.name
        assert payload['sender']['avatar'] == VIBER_BOT_CONFIGURATION.avatar
        assert payload['text'] == text
        return dict(status=0, message_token=message_token)

    request_sender = Mock()
    request_sender.post_request = post_request

    text_message = TextMessage(text=text)

    message_sender = MessageSender(logger, request_sender)
    token = await message_sender.post_to_public_account(
        sender, VIBER_BOT_CONFIGURATION.name, VIBER_BOT_CONFIGURATION.avatar, text_message)
    assert token == message_token


async def test_message_invalid():
    to = '012345A='

    async def post_request(endpoint, payload):
        pytest.fail('message sender not supposed to call post_request')

    request_sender = Mock()
    request_sender.post_request = post_request

    text_message = TextMessage(text=None)

    message_sender = MessageSender(logger, request_sender)
    with pytest.raises(Exception) as exc_info:
        await message_sender.send_message(to, VIBER_BOT_CONFIGURATION.name, VIBER_BOT_CONFIGURATION.avatar, text_message)

    assert str(exc_info.value).startswith('failed validating message:')


async def test_send_message_failed():
    to = '012345A='
    text = 'hi!'

    async def post_request(endpoint, payload):
        raise Exception('failed with status: 1, message: failed')

    request_sender = Mock()
    request_sender.post_request = post_request

    text_message = TextMessage(text=text)

    message_sender = MessageSender(logger, request_sender)
    with pytest.raises(Exception) as exc_info:
        await message_sender.send_message(to, VIBER_BOT_CONFIGURATION.name, VIBER_BOT_CONFIGURATION.avatar, text_message)

    assert str(exc_info.value) == 'failed with status: 1, message: failed'


async def test_post_message_to_public_account_failed():
    sender = '012345A='
    text = 'hi!'

    async def post_request(endpoint, payload):
        raise Exception('failed with status: 1, message: failed')

    request_sender = Mock()
    request_sender.post_request = post_request

    text_message = TextMessage(text=text)

    message_sender = MessageSender(logger, request_sender)
    with pytest.raises(Exception) as exc_info:
        await message_sender.post_to_public_account(
            sender, VIBER_BOT_CONFIGURATION.name, VIBER_BOT_CONFIGURATION.avatar, text_message)

    assert str(exc_info.value) == 'failed with status: 1, message: failed'
