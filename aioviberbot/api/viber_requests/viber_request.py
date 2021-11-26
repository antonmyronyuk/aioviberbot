

class ViberRequest:
    def __init__(self, event_type=None):
        self._event_type = event_type
        self._timestamp = None

    def from_dict(self, request_dict):
        self._timestamp = request_dict['timestamp']
        if self._event_type is None:
            self._event_type = request_dict['event']
        return self

    @property
    def event_type(self):
        return self._event_type

    @property
    def timestamp(self):
        return self._timestamp

    def __str__(self):
        return 'event_type={0}, timestamp={1}'.format(self._event_type, self._timestamp)
