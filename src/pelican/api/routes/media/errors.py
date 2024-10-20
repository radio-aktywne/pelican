from uuid import UUID


class ServiceError(Exception):
    """Base class for service errors."""

    pass


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


class GraphiteError(ServiceError):
    """Raised when a graphite database error occurs."""

    pass


class MiniumError(ServiceError):
    """Raised when an minium database error occurs."""

    pass
