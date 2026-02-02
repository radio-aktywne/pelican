class ServiceError(Exception):
    """Base class for service errors."""


class ValidationError(ServiceError):
    """Raised when a validation error occurs."""


class GraphiteError(ServiceError):
    """Raised when a graphite database operation fails."""


class MiniumError(ServiceError):
    """Raised when a minium database operation fails."""
