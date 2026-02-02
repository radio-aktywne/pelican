class ServiceError(Exception):
    """Base class for service errors."""


class ValidationError(ServiceError):
    """Raised when a validation error occurs."""


class InvalidRankError(ValidationError):
    """Raised when a rank is invalid."""

    def __init__(self, value: str) -> None:
        super().__init__(f"Rank is not a valid fractional indexing key: {value}.")


class GraphiteError(ServiceError):
    """Raised when a graphite database operation fails."""
