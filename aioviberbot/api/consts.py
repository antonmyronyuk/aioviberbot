from ..version import __version__

VIBER_BOT_API_URL = 'https://chatapi.viber.com/pa'
VIBER_BOT_USER_AGENT = 'AioViberBot-Python/' + __version__
BROADCAST_LIST_MAX_LENGTH = 300


class BOT_API_ENDPOINT:
    SET_WEBHOOK = 'set_webhook'
    GET_ACCOUNT_INFO = 'get_account_info'
    SEND_MESSAGE = 'send_message'
    GET_ONLINE = 'get_online'
    GET_USER_DETAILS = 'get_user_details'
    POST = 'post'
    BROADCAST_MESSAGE = 'broadcast_message'
