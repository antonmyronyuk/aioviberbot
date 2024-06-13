import asyncio
import traceback

import aiohttp

from aioviberbot.api.consts import BOT_API_ENDPOINT
from aioviberbot.api.errors import (
    ViberClientError,
    ViberRequestError,
    ViberTimeoutError,
    ViberValidationError,
)


class ApiRequestSender:
    def __init__(
            self,
            logger,
            viber_bot_api_url,
            bot_configuration,
            viber_bot_user_agent,
            client_session=None,
    ):
        self._logger = logger
        self._viber_bot_api_url = viber_bot_api_url
        self._bot_configuration = bot_configuration
        self._user_agent = viber_bot_user_agent
        self._client_session = client_session

    async def post_request(self, endpoint, payload=None):
        url = self._viber_bot_api_url + '/' + endpoint
        payload = payload or {}
        payload['auth_token'] = self._bot_configuration.auth_token
        headers = {'User-Agent': self._user_agent}

        if self._client_session:
            session = self._client_session
        else:
            session = aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(10))

        try:
            response = await session.post(
                url=url,
                json=payload,
                headers=headers,
            )
            response.raise_for_status()
            result = await response.json()
        except aiohttp.ClientError as e:
            self._logger.error(
                'client error on post request to endpoint={0}, with payload={1}. error is: {2}'
                .format(endpoint, payload, traceback.format_exc()),
            )
            raise ViberClientError(e)
        except asyncio.TimeoutError as e:
            self._logger.error(
                'timeout error on post request to endpoint={0}, with payload={1}. error is: {2}'
                .format(endpoint, payload, traceback.format_exc()),
            )
            raise ViberTimeoutError(e)
        except Exception:
            self._logger.error(
                'unexpected Exception while trying to post request. error is: {0}'
                .format(traceback.format_exc()),
            )
            raise
        else:
            if result['status'] == 0:
                return result

            raise ViberRequestError(
                'failed with status: {0}, message: {1}'
                .format(result['status'], result.get('status_message')),
            )
        finally:
            if not self._client_session:
                await session.close()

    async def set_webhook(self, url, webhook_events=None, is_inline=False, send_name=True, send_photo=True):
        payload = {
            'url': url,
            'is_inline': is_inline,
            'send_name': send_name,
            'send_photo': send_photo,
        }

        if webhook_events is not None:
            if not isinstance(webhook_events, list):
                webhook_events = [webhook_events]
            payload['event_types'] = webhook_events

        result = await self.post_request(
            endpoint=BOT_API_ENDPOINT.SET_WEBHOOK,
            payload=payload,
        )
        return result['event_types']

    async def get_account_info(self):
        return await self.post_request(BOT_API_ENDPOINT.GET_ACCOUNT_INFO)

    async def get_online_status(self, ids):
        if ids is None or not isinstance(ids, list) or len(ids) == 0:
            raise ViberValidationError('missing parameter ids, should be a list of viber memberIds')

        payload = {
            'ids': ids,
        }
        result = await self.post_request(
            endpoint=BOT_API_ENDPOINT.GET_ONLINE,
            payload=payload,
        )
        return result['users']

    async def get_user_details(self, user_id):
        if user_id is None:
            raise ViberValidationError('missing parameter id')

        payload = {
            'id': user_id,
        }
        result = await self.post_request(
            endpoint=BOT_API_ENDPOINT.GET_USER_DETAILS,
            payload=payload,
        )
        return result['user']
