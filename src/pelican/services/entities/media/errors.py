from pelican.utils.mime import MimeType


class ServiceError(Exception):
    """Base class for service errors."""


class ValidationError(ServiceError):
    """Raised when a validation error occurs."""


class UnsupportedContentTypeError(ValidationError):
    """Raised when an unsupported content type is provided."""

    def __init__(self, content_type: MimeType) -> None:
        super().__init__(f"Unsupported content type: {content_type!s}.")


class ConflictError(ValidationError):
    """Raised when a conflict error occurs."""
