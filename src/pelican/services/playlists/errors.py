class ServiceError(Exception):
    """Base class for service errors."""


class ValidationError(ServiceError):
    """Raised when a request fails validation."""


class GraphiteError(ServiceError):
    """Raised when a graphite database operation fails."""
