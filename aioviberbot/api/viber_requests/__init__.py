from aioviberbot.api.errors import ViberValidationError
from aioviberbot.api.event_type import EventType
from aioviberbot.api.viber_requests.viber_conversation_started_request import ViberConversationStartedRequest
from aioviberbot.api.viber_requests.viber_delivered_request import ViberDeliveredRequest
from aioviberbot.api.viber_requests.viber_failed_request import ViberFailedRequest
from aioviberbot.api.viber_requests.viber_message_request import ViberMessageRequest
from aioviberbot.api.viber_requests.viber_request import ViberRequest
from aioviberbot.api.viber_requests.viber_seen_request import ViberSeenRequest
from aioviberbot.api.viber_requests.viber_subscribed_request import ViberSubscribedRequest
from aioviberbot.api.viber_requests.viber_unsubscribed_request import ViberUnsubscribedRequest

EVENT_TYPE_TO_CLASS = {
    EventType.MESSAGE: ViberMessageRequest,
    EventType.FAILED: ViberFailedRequest,
    EventType.CONVERSATION_STARTED: ViberConversationStartedRequest,
    EventType.DELIVERED: ViberDeliveredRequest,
    EventType.SEEN: ViberSeenRequest,
    EventType.SUBSCRIBED: ViberSubscribedRequest,
    EventType.UNSUBSCRIBED: ViberUnsubscribedRequest,
    EventType.WEBHOOK: ViberRequest
}


def create_request(request_dict):
    if 'event' not in request_dict:
        raise ViberValidationError("request is missing field 'event'")

    if request_dict['event'] not in EVENT_TYPE_TO_CLASS:
        raise ViberValidationError(
            "event type '{0}' is not supported".format(request_dict['event']),
        )

    return EVENT_TYPE_TO_CLASS[request_dict['event']]().from_dict(request_dict)


__all__ = [
    'ViberConversationStartedRequest', 'ViberDeliveredRequest', 'ViberFailedRequest', 'ViberMessageRequest',
    'ViberSeenRequest', 'ViberSubscribedRequest', 'ViberUnsubscribedRequest', 'create_request',
]
