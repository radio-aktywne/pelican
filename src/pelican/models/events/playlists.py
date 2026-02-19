from typing import Literal, Self
from uuid import UUID

from pydantic import Field

from pelican.models.base import SerializableModel
from pelican.models.events.enums import EventType
from pelican.models.events.fields import CreatedAtField, DataField, TypeField
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

    type: TypeField[Literal[EventType.PLAYLIST_CREATED]] = EventType.PLAYLIST_CREATED
    created_at: CreatedAtField = Field(default_factory=naiveutcnow)
    data: DataField[PlaylistCreatedEventData]


class PlaylistUpdatedEventData(SerializableModel):
    """Data of a playlist updated event."""

    playlist: Playlist
    """Playlist that was updated."""


class PlaylistUpdatedEvent(SerializableModel):
    """Event that is emitted when playlist is updated."""

    type: TypeField[Literal[EventType.PLAYLIST_UPDATED]] = EventType.PLAYLIST_UPDATED
    created_at: CreatedAtField = Field(default_factory=naiveutcnow)
    data: DataField[PlaylistUpdatedEventData]


class PlaylistDeletedEventData(SerializableModel):
    """Data of a playlist deleted event."""

    playlist: Playlist
    """Playlist that was deleted."""


class PlaylistDeletedEvent(SerializableModel):
    """Event that is emitted when playlist is deleted."""

    type: TypeField[Literal[EventType.PLAYLIST_DELETED]] = EventType.PLAYLIST_DELETED
    created_at: CreatedAtField = Field(default_factory=naiveutcnow)
    data: DataField[PlaylistDeletedEventData]
