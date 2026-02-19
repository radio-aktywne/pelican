from enum import StrEnum


class EventType(StrEnum):
    """Event types."""

    TEST = "test"
    BINDING_CREATED = "binding-created"
    BINDING_UPDATED = "binding-updated"
    BINDING_DELETED = "binding-deleted"
    MEDIA_CREATED = "media-created"
    MEDIA_UPDATED = "media-updated"
    MEDIA_DELETED = "media-deleted"
    PLAYLIST_CREATED = "playlist-created"
    PLAYLIST_UPDATED = "playlist-updated"
    PLAYLIST_DELETED = "playlist-deleted"
