from aioviberbot.api.event_type import EventType
from aioviberbot.api.viber_requests.viber_request import ViberRequest


class ViberUnsubscribedRequest(ViberRequest):
	def __init__(self):
		super(ViberUnsubscribedRequest, self).__init__(EventType.UNSUBSCRIBED)
		self._user_id = None

	def from_dict(self, request_dict):
		super(ViberUnsubscribedRequest, self).from_dict(request_dict)
		self._user_id = request_dict['user_id']
		return self

	@property
	def user_id(self):
		return self._user_id

	def __str__(self):
		return u"ViberUnsubscribedRequest [{0}, user_id={1}]" \
			.format(super(ViberUnsubscribedRequest, self).__str__(), self._user_id)
