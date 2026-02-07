from typing import Literal, Self
from uuid import UUID

from pydantic import Field

from pelican.models.base import SerializableModel
from pelican.models.events import types as t
from pelican.services.playlists import models as pm
from pelican.utils.time import naiveutcnow


class Playlist(SerializableModel):
    """Playlist data."""

    id: UUID
    """Identifier of the playlist."""

    name: str
    """Name of the playlist."""

    @classmethod
    def map(cls, playlist: pm.Playlist) -> Self:
        """Map to internal representation."""
        return cls(id=UUID(playlist.id), name=playlist.name)


class PlaylistCreatedEventData(SerializableModel):
    """Data of a playlist created event."""

    playlist: Playlist
    """Playlist that was created."""


class PlaylistCreatedEvent(SerializableModel):
    """Event that is emitted when playlist is created."""

    type: t.TypeField[Literal["playlist-created"]] = "playlist-created"
    created_at: t.CreatedAtField = Field(default_factory=naiveutcnow)
    data: t.DataField[PlaylistCreatedEventData]


class PlaylistUpdatedEventData(SerializableModel):
    """Data of a playlist updated event."""

    playlist: Playlist
    """Playlist that was updated."""


class PlaylistUpdatedEvent(SerializableModel):
    """Event that is emitted when playlist is updated."""

    type: t.TypeField[Literal["playlist-updated"]] = "playlist-updated"
    created_at: t.CreatedAtField = Field(default_factory=naiveutcnow)
    data: t.DataField[PlaylistUpdatedEventData]


class PlaylistDeletedEventData(SerializableModel):
    """Data of a playlist deleted event."""

    playlist: Playlist
    """Playlist that was deleted."""


class PlaylistDeletedEvent(SerializableModel):
    """Event that is emitted when playlist is deleted."""

    type: t.TypeField[Literal["playlist-deleted"]] = "playlist-deleted"
    created_at: t.CreatedAtField = Field(default_factory=naiveutcnow)
    data: t.DataField[PlaylistDeletedEventData]
