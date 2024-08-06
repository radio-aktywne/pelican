class ServiceError(Exception):
    """Base class for service errors."""

    pass


class ValidationError(ServiceError):
    """Raised when a request fails validation."""

    pass


class DatatunesError(ServiceError):
    """Raised when a datatunes database operation fails."""

    pass


class MediatunesError(ServiceError):
    """Raised when a mediatunes database operation fails."""

    pass
