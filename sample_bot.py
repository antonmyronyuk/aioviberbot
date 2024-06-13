from aiohttp import web

from aioviberbot import Api
from aioviberbot.api.bot_configuration import BotConfiguration
from aioviberbot.api.messages.text_message import TextMessage
from aioviberbot.api.viber_requests import ViberConversationStartedRequest
from aioviberbot.api.viber_requests import ViberMessageRequest
from aioviberbot.api.viber_requests import ViberSubscribedRequest

viber = Api(BotConfiguration(
    name='PythonSampleBot',
    avatar='http://viber.com/avatar.jpg',
    auth_token='YOUR_AUTH_TOKEN_HERE'
))


async def webhook(request: web.Request) -> web.Response:
    request_data = await request.read()
    signature = request.headers.get('X-Viber-Content-Signature')
    if not viber.verify_signature(request_data, signature):
        raise web.HTTPForbidden

    viber_request = viber.parse_request(request_data)
    if isinstance(viber_request, ViberMessageRequest):
        # echo message
        await viber.send_messages(
            viber_request.sender.id,
            [viber_request.message],
        )
    elif isinstance(viber_request, ViberSubscribedRequest):
        await viber.send_messages(
            viber_request.user.id,
            [TextMessage(text='Thanks for subscribing!')],
        )
    elif isinstance(viber_request, ViberConversationStartedRequest):
        await viber.send_messages(
            viber_request.user.id,
            [TextMessage(text='Thanks for starting conversation!')],
        )

    return web.json_response({'ok': True})


async def set_webhook_signal(app: web.Application):
    await viber.set_webhook('https://mybotwebserver.com/webhook')


if __name__ == '__main__':
    app = web.Application()
    app.on_startup.append(set_webhook_signal)
    app.router.add_route('POST', '/webhook', webhook),
    web.run_app(app)
