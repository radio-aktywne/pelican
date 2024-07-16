from uuid import UUID


class ServiceError(Exception):
    """Base class for service errors."""

    def __init__(self, message: str | None = None) -> None:
        self._message = message

        args = (message,) if message else ()
        super().__init__(*args)

    @property
    def message(self) -> str | None:
        return self._message


class ValidationError(ServiceError):
    """Raised when a validation error occurs."""

    pass


class MediaNotFoundError(ServiceError):
    """Raised when media is not found."""

    def __init__(self, id: UUID) -> None:
        super().__init__(f"Media not found: {id}.")


class ContentNotFoundError(ServiceError):
    """Raised when content is not found."""

    def __init__(self, id: UUID) -> None:
        super().__init__(f"Content not found for media: {id}.")


class DatatunesError(ServiceError):
    """Raised when a datatunes database error occurs."""

    pass


class MediatunesError(ServiceError):
    """Raised when an mediatunes database error occurs."""

    pass
