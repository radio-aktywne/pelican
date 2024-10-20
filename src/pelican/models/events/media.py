from typing import Literal
from uuid import UUID

from pelican.models.base import SerializableModel
from pelican.models.events import types as t
from pelican.services.media import models as mm


class Media(SerializableModel):
    """Media data."""

    id: UUID
    """Identifier of the media."""

    name: str
    """Name of the media."""

    @staticmethod
    def map(media: mm.Media) -> "Media":
        return Media(
            id=media.id,
            name=media.name,
        )


class MediaCreatedEventData(SerializableModel):
    """Data of a media created event."""

    media: Media
    """Media that was created."""


class MediaCreatedEvent(SerializableModel):
    """Event that is emitted when media is created."""

    type: t.TypeFieldType[Literal["media-created"]] = "media-created"
    created_at: t.CreatedAtFieldType
    data: t.DataFieldType[MediaCreatedEventData]


class MediaUpdatedEventData(SerializableModel):
    """Data of a media updated event."""

    media: Media
    """Media that was updated."""


class MediaUpdatedEvent(SerializableModel):
    """Event that is emitted when media is updated."""

    type: t.TypeFieldType[Literal["media-updated"]] = "media-updated"
    created_at: t.CreatedAtFieldType
    data: t.DataFieldType[MediaUpdatedEventData]


class MediaDeletedEventData(SerializableModel):
    """Data of a media deleted event."""

    media: Media
    """Media that was deleted."""


class MediaDeletedEvent(SerializableModel):
    """Event that is emitted when media is deleted."""

    type: t.TypeFieldType[Literal["media-deleted"]] = "media-deleted"
    created_at: t.CreatedAtFieldType
    data: t.DataFieldType[MediaDeletedEventData]
