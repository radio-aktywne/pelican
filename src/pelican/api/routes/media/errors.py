from uuid import UUID


class ServiceError(Exception):
    """Base class for service errors."""


class ValidationError(ServiceError):
    """Raised when a validation error occurs."""


class MediaNotFoundError(ServiceError):
    """Raised when media is not found."""

    def __init__(self, media_id: UUID) -> None:
        super().__init__(f"Media not found: {media_id}.")


class ContentNotFoundError(ServiceError):
    """Raised when content is not found."""

    def __init__(self, media_id: UUID) -> None:
        super().__init__(f"Content not found for media: {media_id}.")


class GraphiteError(ServiceError):
    """Raised when a graphite database error occurs."""


class MiniumError(ServiceError):
    """Raised when an minium database error occurs."""
