from typing import Literal

from emitunes.models.base import SerializableModel
from emitunes.models.events import types as t
from emitunes.services.playlists import models as pm


class Playlist(SerializableModel):
    """Playlist data."""

    id: str
    """Identifier of the playlist."""

    name: str
    """Name of the playlist."""

    @staticmethod
    def map(playlist: pm.Playlist) -> "Playlist":
        return Playlist(
            id=playlist.id,
            name=playlist.name,
        )


class PlaylistCreatedEventData(SerializableModel):
    """Data of a playlist created event."""

    playlist: Playlist
    """Playlist that was created."""


class PlaylistCreatedEvent(SerializableModel):
    """Event that is emitted when playlist is created."""

    type: t.TypeFieldType[Literal["playlist-created"]] = "playlist-created"
    created_at: t.CreatedAtFieldType
    data: t.DataFieldType[PlaylistCreatedEventData]


class PlaylistUpdatedEventData(SerializableModel):
    """Data of a playlist updated event."""

    playlist: Playlist
    """Playlist that was updated."""


class PlaylistUpdatedEvent(SerializableModel):
    """Event that is emitted when playlist is updated."""

    type: t.TypeFieldType[Literal["playlist-updated"]] = "playlist-updated"
    created_at: t.CreatedAtFieldType
    data: t.DataFieldType[PlaylistUpdatedEventData]


class PlaylistDeletedEventData(SerializableModel):
    """Data of a playlist deleted event."""

    playlist: Playlist
    """Playlist that was deleted."""


class PlaylistDeletedEvent(SerializableModel):
    """Event that is emitted when playlist is deleted."""

    type: t.TypeFieldType[Literal["playlist-deleted"]] = "playlist-deleted"
    created_at: t.CreatedAtFieldType
    data: t.DataFieldType[PlaylistDeletedEventData]
