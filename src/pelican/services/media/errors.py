class ServiceError(Exception):
    """Base class for service errors."""

    pass


class ValidationError(ServiceError):
    """Raised when a request fails validation."""

    pass


class GraphiteError(ServiceError):
    """Raised when a graphite database operation fails."""

    pass


class MiniumError(ServiceError):
    """Raised when a minium database operation fails."""

    pass
