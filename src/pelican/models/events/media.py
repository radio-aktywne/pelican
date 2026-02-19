from typing import Literal, Self
from uuid import UUID

from pydantic import Field

from pelican.models.base import SerializableModel
from pelican.models.events.enums import EventType
from pelican.models.events.fields import CreatedAtField, DataField, TypeField
from pelican.services.media import models as mm
from pelican.utils.time import naiveutcnow


class Media(SerializableModel):
    """Media data."""

    id: UUID
    """Identifier of the media."""

    name: str
    """Name of the media."""

    @classmethod
    def map(cls, media: mm.Media) -> Self:
        """Map to internal representation."""
        return cls(id=UUID(media.id), name=media.name)


class MediaCreatedEventData(SerializableModel):
    """Data of a media created event."""

    media: Media
    """Media that was created."""


class MediaCreatedEvent(SerializableModel):
    """Event that is emitted when media is created."""

    type: TypeField[Literal[EventType.MEDIA_CREATED]] = EventType.MEDIA_CREATED
    created_at: CreatedAtField = Field(default_factory=naiveutcnow)
    data: DataField[MediaCreatedEventData]


class MediaUpdatedEventData(SerializableModel):
    """Data of a media updated event."""

    media: Media
    """Media that was updated."""


class MediaUpdatedEvent(SerializableModel):
    """Event that is emitted when media is updated."""

    type: TypeField[Literal[EventType.MEDIA_UPDATED]] = EventType.MEDIA_UPDATED
    created_at: CreatedAtField = Field(default_factory=naiveutcnow)
    data: DataField[MediaUpdatedEventData]


class MediaDeletedEventData(SerializableModel):
    """Data of a media deleted event."""

    media: Media
    """Media that was deleted."""


class MediaDeletedEvent(SerializableModel):
    """Event that is emitted when media is deleted."""

    type: TypeField[Literal[EventType.MEDIA_DELETED]] = EventType.MEDIA_DELETED
    created_at: CreatedAtField = Field(default_factory=naiveutcnow)
    data: DataField[MediaDeletedEventData]
