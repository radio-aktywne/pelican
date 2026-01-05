from uuid import UUID


class ServiceError(Exception):
    """Base class for service errors."""


class ValidationError(ServiceError):
    """Raised when a validation error occurs."""


class BindingNotFoundError(ServiceError):
    """Raised when binding is not found."""

    def __init__(self, binding_id: UUID) -> None:
        super().__init__(f"Binding not found: {binding_id}.")


class GraphiteError(ServiceError):
    """Raised when a graphite database error occurs."""
