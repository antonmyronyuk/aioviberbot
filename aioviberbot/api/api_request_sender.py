import asyncio
import json
import traceback

import aiohttp

from aioviberbot.api.consts import BOT_API_ENDPOINT


class ApiRequestSender:
	def __init__(self, logger, viber_bot_api_url, bot_configuration, viber_bot_user_agent):
		self._logger = logger
		self._viber_bot_api_url = viber_bot_api_url
		self._bot_configuration = bot_configuration
		self._user_agent = viber_bot_user_agent

	async def set_webhook(self, url, webhook_events=None, is_inline=False):
		payload = {
			'auth_token': self._bot_configuration.auth_token,
			'url': url,
			'is_inline': is_inline
		}

		if webhook_events is not None:
			if not isinstance(webhook_events, list):
				webhook_events = [webhook_events]
			payload['event_types'] = webhook_events

		result = await self.post_request(
			endpoint=BOT_API_ENDPOINT.SET_WEBHOOK,
			payload=json.dumps(payload))

		if not result['status'] == 0:
			raise Exception(u"failed with status: {0}, message: {1}".format(result['status'], result['status_message']))

		return result['event_types']

	async def get_account_info(self):
		payload = {
			'auth_token': self._bot_configuration.auth_token
		}
		return await self.post_request(
			endpoint=BOT_API_ENDPOINT.GET_ACCOUNT_INFO,
			payload=json.dumps(payload))

	async def post_request(self, endpoint, payload):
		url = self._viber_bot_api_url + '/' + endpoint
		headers = {'User-Agent': self._user_agent}
		async with aiohttp.ClientSession() as session:
			try:
				response = await session.post(
					url=url,
					data=payload,
					headers=headers,
				)
				response.raise_for_status()
				return await response.json()
			except (aiohttp.ClientError, asyncio.TimeoutError):
				self._logger.error(
					"failed to post request to endpoint={0}, with payload={1}. error is: {2}"
					.format(endpoint, payload, traceback.format_exc())
				)
				raise

	async def get_online_status(self, ids=[]):
		if ids is None or not isinstance(ids, list) or len(ids) == 0:
			raise Exception(u"missing parameter ids, should be a list of viber memberIds")

		payload = {
			'auth_token': self._bot_configuration.auth_token,
			'ids': ids
		}
		result = await self.post_request(
			endpoint=BOT_API_ENDPOINT.GET_ONLINE,
			payload=json.dumps(payload))

		if not result['status'] == 0:
			raise Exception(u"failed with status: {0}, message: {1}".format(result['status'], result['status_message']))

		return result['users']

	async def get_user_details(self, user_id):
		if user_id is None:
			raise Exception(u"missing parameter id")

		payload = {
			'auth_token': self._bot_configuration.auth_token,
			'id': user_id
		}
		result = await self.post_request(
			endpoint=BOT_API_ENDPOINT.GET_USER_DETAILS,
			payload=json.dumps(payload))

		if not result['status'] == 0:
			raise Exception(u"failed with status: {0}, message: {1}".format(result['status'], result['status_message']))

		return result['user']


