from aioviberbot.api.messages.typed_message import TypedMessage
from aioviberbot.api.messages.message_type import MessageType


class TextMessage(TypedMessage):
    def __init__(self, tracking_data=None, keyboard=None, text=None, min_api_version=None):
        super(TextMessage, self).__init__(MessageType.TEXT, tracking_data, keyboard, min_api_version)
        self._text = text

    def to_dict(self):
        message_data = super(TextMessage, self).to_dict()
        message_data['text'] = self._text
        return message_data

    def from_dict(self, message_data):
        super(TextMessage, self).from_dict(message_data)
        if 'text' in message_data:
            self._text = message_data['text']
        return self

    def validate(self):
        return super(TextMessage, self).validate() \
                and self._text is not None

    @property
    def text(self):
        return self._text

    def __str__(self):
        return 'TextMessage [{0}, text={1}]'.format(super(TextMessage, self).__str__(), self._text)
