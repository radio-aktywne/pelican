from uuid import UUID


class ServiceError(Exception):
    """Base class for service errors."""

    pass


class ValidationError(ServiceError):
    """Raised when a validation error occurs."""

    pass


class BindingNotFoundError(ServiceError):
    """Raised when binding is not found."""

    def __init__(self, id: UUID) -> None:
        super().__init__(f"Binding not found: {id}.")


class GraphiteError(ServiceError):
    """Raised when a graphite database error occurs."""

    pass
