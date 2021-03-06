from aioviberbot.api.messages.message import Message


class KeyboardMessage(Message):
    def __init__(self, tracking_data=None, keyboard=None, min_api_version=None):
        super(KeyboardMessage, self).__init__(tracking_data, keyboard, min_api_version)

    def to_dict(self):
        return super(KeyboardMessage, self).to_dict()

    def from_dict(self, message_data):
        super(KeyboardMessage, self).from_dict(message_data)
        return self

    def validate(self):
        return self._keyboard is not None

    def __str__(self):
        return 'KeyboardMessage [{0}]'.format(super(KeyboardMessage, self).__str__())
