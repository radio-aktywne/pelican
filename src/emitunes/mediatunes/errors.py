class MediatunesError(Exception):
    """Base class for mediatunes errors."""

    def __init__(self, message: str | None = None) -> None:
        self._message = message

        args = (message,) if message else ()
        super().__init__(*args)

    @property
    def message(self) -> str | None:
        return self._message


class NotFoundError(MediatunesError):
    """Raised when an object is not found."""

    def __init__(self, name: str) -> None:
        super().__init__(f"Object not found: {name}.")
