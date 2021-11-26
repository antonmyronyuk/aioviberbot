import typing as t


class ResponseStub:
    def __init__(self, return_value: t.Any) -> None:
        self.return_value = return_value

    def raise_for_status(self) -> None:
        pass

    async def json(self) -> t.Any:
        return self.return_value
