import json
import logging
import sys

import aiohttp
import pytest

from aioviberbot.api.api_request_sender import ApiRequestSender
from aioviberbot.api.bot_configuration import BotConfiguration
from aioviberbot.api.consts import BOT_API_ENDPOINT, VIBER_BOT_USER_AGENT
from aioviberbot.api.event_type import EventType
from .stubs import ResponseStub

if sys.version_info < (3, 8):
    from asynctest import patch
else:
    from unittest.mock import patch

logger = logging.getLogger('super-logger')
VIBER_BOT_API_URL = 'http://site.com'
VIBER_BOT_CONFIGURATION = BotConfiguration(
    auth_token='auth-token-sample',
    name='testbot',
    avatar='https://avatars.com/avatar.jpg',
)


async def test_set_webhook_sanity():
    webhook_events = [EventType.DELIVERED, EventType.UNSUBSCRIBED, EventType.SEEN]
    url = 'http://sample.url.com'

    async def post_request(endpoint, payload):
        assert endpoint == BOT_API_ENDPOINT.SET_WEBHOOK
        assert payload['event_types'] == webhook_events
        assert payload['url'] == url
        return dict(status=0, event_types=webhook_events)

    request_sender = ApiRequestSender(logger, VIBER_BOT_API_URL, VIBER_BOT_CONFIGURATION, VIBER_BOT_USER_AGENT)
    request_sender.post_request = post_request

    response = await request_sender.set_webhook(url=url, webhook_events=webhook_events)
    assert response == webhook_events


async def test_set_webhook_failure():
    webhook_events = [EventType.DELIVERED, EventType.UNSUBSCRIBED, EventType.SEEN]
    url = 'http://sample.url.com'

    async def post_request(endpoint, payload):
        raise Exception('failed with status: 1, message: failed')

    request_sender = ApiRequestSender(logger, VIBER_BOT_API_URL, VIBER_BOT_CONFIGURATION, VIBER_BOT_USER_AGENT)
    request_sender.post_request = post_request
    with pytest.raises(Exception) as exc_info:
        await request_sender.set_webhook(url=url, webhook_events=webhook_events)

    assert str(exc_info.value) == 'failed with status: 1, message: failed'


async def test_post_request_success_exsisting_client_session(monkeypatch):
    account_id = 'pa:54321'
    client_session = aiohttp.ClientSession()

    async def callback(session, url, json, headers, *args, **kwargs):
        assert url == VIBER_BOT_API_URL + '/' + BOT_API_ENDPOINT.GET_ACCOUNT_INFO
        assert json['auth_token'] == VIBER_BOT_CONFIGURATION.auth_token
        assert headers['User-Agent'] == VIBER_BOT_USER_AGENT
        return ResponseStub({
            'status': 0,
            'status_message': 'ok',
            'id': account_id,
        })

    monkeypatch.setattr('aiohttp.ClientSession.post', callback)
    request_sender = ApiRequestSender(
        logger=logger,
        viber_bot_api_url=VIBER_BOT_API_URL,
        bot_configuration=VIBER_BOT_CONFIGURATION,
        viber_bot_user_agent=VIBER_BOT_USER_AGENT,
        client_session=client_session,
    )

    with patch('aiohttp.ClientSession.close') as close_session_mock:
        response = await request_sender.get_account_info()
        assert response['id'] == account_id
        close_session_mock.assert_not_called()


async def test_post_request_success(monkeypatch):
    account_id = 'pa:12345'

    async def callback(session, url, json, headers, *args, **kwargs):
        assert url == VIBER_BOT_API_URL + '/' + BOT_API_ENDPOINT.GET_ACCOUNT_INFO
        assert json['auth_token'] == VIBER_BOT_CONFIGURATION.auth_token
        assert headers['User-Agent'] == VIBER_BOT_USER_AGENT
        return ResponseStub({
            'status': 0,
            'status_message': 'ok',
            'id': account_id,
        })

    monkeypatch.setattr('aiohttp.ClientSession.post', callback)
    request_sender = ApiRequestSender(logger, VIBER_BOT_API_URL, VIBER_BOT_CONFIGURATION, VIBER_BOT_USER_AGENT)

    with patch('aiohttp.ClientSession.close') as close_session_mock:
        response = await request_sender.get_account_info()
        assert response['id'] == account_id
        close_session_mock.assert_called_once()


async def test_post_request_json_exception(monkeypatch):
    async def json_decode_error_mock():
        return json.loads('not a json')

    async def callback(session, url, json, headers, *args, **kwargs):
        assert url == VIBER_BOT_API_URL + '/' + BOT_API_ENDPOINT.GET_ACCOUNT_INFO
        assert json['auth_token'] == VIBER_BOT_CONFIGURATION.auth_token
        assert headers['User-Agent'] == VIBER_BOT_USER_AGENT
        response = ResponseStub({})
        response.json = json_decode_error_mock
        return response

    monkeypatch.setattr('aiohttp.ClientSession.post', callback)
    request_sender = ApiRequestSender(logger, VIBER_BOT_API_URL, VIBER_BOT_CONFIGURATION, VIBER_BOT_USER_AGENT)

    with pytest.raises(Exception) as exc_info:
        await request_sender.get_account_info()

    assert issubclass(exc_info.type, json.JSONDecodeError)


async def test_get_online_status_fail(monkeypatch):
    user_ids = ['0123456789=']

    async def callback(session, url, json, headers, *args, **kwargs):
        assert url == VIBER_BOT_API_URL + '/' + BOT_API_ENDPOINT.GET_ONLINE
        assert json['auth_token'] == VIBER_BOT_CONFIGURATION.auth_token
        assert json['ids'] == user_ids
        assert headers['User-Agent'] == VIBER_BOT_USER_AGENT
        return ResponseStub({
            'status': 1,
            'status_message': 'failed',
        })

    monkeypatch.setattr('aiohttp.ClientSession.post', callback)
    request_sender = ApiRequestSender(logger, VIBER_BOT_API_URL, VIBER_BOT_CONFIGURATION, VIBER_BOT_USER_AGENT)

    with pytest.raises(Exception) as exc_info:
        await request_sender.get_online_status(ids=user_ids)

    assert str(exc_info.value) == 'failed with status: 1, message: failed'


async def test_get_online_missing_ids(monkeypatch):
    async def callback(session, url, json, headers, *args, **kwargs):
        pytest.fail('request sender not supposed to call post_request')

    monkeypatch.setattr('aiohttp.ClientSession.post', callback)
    request_sender = ApiRequestSender(logger, VIBER_BOT_API_URL, VIBER_BOT_CONFIGURATION, VIBER_BOT_USER_AGENT)

    with pytest.raises(Exception) as exc_info:
        await request_sender.get_online_status(ids=None)

    assert str(exc_info.value) == 'missing parameter ids, should be a list of viber memberIds'


async def test_get_online_success(monkeypatch):
    user_ids = ['03249305A=']

    async def callback(session, url, json, headers, *args, **kwargs):
        assert url == VIBER_BOT_API_URL + '/' + BOT_API_ENDPOINT.GET_ONLINE
        assert json['auth_token'] == VIBER_BOT_CONFIGURATION.auth_token
        assert json['ids'] == user_ids
        assert headers['User-Agent'] == VIBER_BOT_USER_AGENT
        return ResponseStub({
            'status': 0,
            'status_message': 'ok',
            'users': [],
        })

    monkeypatch.setattr('aiohttp.ClientSession.post', callback)
    request_sender = ApiRequestSender(logger, VIBER_BOT_API_URL, VIBER_BOT_CONFIGURATION, VIBER_BOT_USER_AGENT)

    response = await request_sender.get_online_status(ids=user_ids)
    assert response == []


async def test_get_user_details_success(monkeypatch):
    user_id = '03249305A='
    user_info = {
        'id': user_id,
        'name': 'Some Name',
        'avatar': 'https://avatar.com/user-avatar.png',
        'language': 'uk',
    }

    async def callback(session, url, json, headers, *args, **kwargs):
        assert url == VIBER_BOT_API_URL + '/' + BOT_API_ENDPOINT.GET_USER_DETAILS
        assert json['auth_token'] == VIBER_BOT_CONFIGURATION.auth_token
        assert json['id'] == user_id
        assert headers['User-Agent'] == VIBER_BOT_USER_AGENT
        return ResponseStub({
            'status': 0,
            'status_message': 'ok',
            'user': user_info,
        })

    monkeypatch.setattr('aiohttp.ClientSession.post', callback)
    request_sender = ApiRequestSender(logger, VIBER_BOT_API_URL, VIBER_BOT_CONFIGURATION, VIBER_BOT_USER_AGENT)

    response = await request_sender.get_user_details(user_id=user_id)
    assert response == user_info
