class ViberError(Exception):
    pass


class ViberValidationError(ViberError):
    pass


class ViberClientError(ViberError):
    pass


class ViberTimeoutError(ViberError):
    pass


class ViberRequestError(ViberError):
    pass
