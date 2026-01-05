from uuid import UUID


class ServiceError(Exception):
    """Base class for service errors."""


class ValidationError(ServiceError):
    """Raised when a validation error occurs."""


class PlaylistNotFoundError(ServiceError):
    """Raised when playlist is not found."""

    def __init__(self, playlist_id: UUID) -> None:
        super().__init__(f"Playlist not found: {playlist_id}.")


class GraphiteError(ServiceError):
    """Raised when a graphite database error occurs."""
