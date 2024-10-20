class ServiceError(Exception):
    """Base class for service errors."""

    pass


class ValidationError(ServiceError):
    """Raised when a request fails validation."""

    pass


class InvalidRankError(ValidationError):
    """Raised when a rank is invalid."""

    def __init__(self, value: str) -> None:
        super().__init__(f"Rank is not a valid fractional indexing key: {value}.")


class GraphiteError(ServiceError):
    """Raised when a graphite database operation fails."""

    pass
