from aioviberbot.api.consts import BOT_API_ENDPOINT


class MessageSender:
    def __init__(self, logger, request_sender):
        self._logger = logger
        self._request_sender = request_sender

    async def send_message(self, to, sender_name, sender_avatar, message, chat_id=None):
        if not message.validate():
            self._logger.error('failed validating message: {0}'.format(message))
            raise Exception('failed validating message: {0}'.format(message))

        payload = self._prepare_payload(
            message=message,
            receiver=to,
            sender_name=sender_name,
            sender_avatar=sender_avatar,
            chat_id=chat_id
        )

        self._logger.debug('going to send message: {0}'.format(payload))

        result = await self._request_sender.post_request(
            BOT_API_ENDPOINT.SEND_MESSAGE, payload,
        )
        return result['message_token']

    async def post_to_public_account(self, sender, sender_name, sender_avatar, message):
        if not message.validate():
            self._logger.error('failed validating message: {0}'.format(message))
            raise Exception('failed validating message: {0}'.format(message))

        if sender is None:
            raise Exception('missing parameter sender')

        payload = self._prepare_payload(
            message=message,
            sender=sender,
            sender_name=sender_name,
            sender_avatar=sender_avatar
        )

        self._logger.debug('going to send message: {0}'.format(payload))

        result = await self._request_sender.post_request(
            BOT_API_ENDPOINT.POST, payload,
        )
        return result['message_token']

    def _prepare_payload(self, message, sender_name, sender_avatar, sender=None, receiver=None, chat_id=None):
        payload = message.to_dict()
        payload.update({
            'from': sender,
            'receiver': receiver,
            'sender': {
                'name': sender_name,
                'avatar': sender_avatar
            },
            'chat_id': chat_id
        })

        return self._remove_empty_fields(payload)

    def _remove_empty_fields(self, message):
        return {k: v for k, v in message.items() if v is not None}
