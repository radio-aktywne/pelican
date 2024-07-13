from datetime import datetime
from typing import Annotated, Literal, TypeVar

from pydantic import Field, RootModel

from emitunes.media import models as mm
from emitunes.models.base import SerializableModel
from emitunes.utils.time import naiveutcnow

TypeType = TypeVar("TypeType")
DataType = TypeVar("DataType", bound=SerializableModel)

TypeFieldType = Annotated[
    TypeType,
    Field(description="Type of the event."),
]
CreatedAtFieldType = Annotated[
    datetime,
    Field(
        default_factory=naiveutcnow, description="Time at which the event was created."
    ),
]
DataFieldType = Annotated[
    DataType,
    Field(description="Data of the event."),
]


class MediaCreatedEventData(SerializableModel):
    """Data of a media created event."""

    media: mm.Media = Field(
        ...,
        title="MediaCreatedEventData.Media",
        description="Media that was created.",
    )


class MediaCreatedEvent(SerializableModel):
    """Event that is emitted when media is created."""

    type: TypeFieldType[Literal["media-created"]] = Field(
        "media-created",
        title="MediaCreatedEvent.Type",
    )
    created_at: CreatedAtFieldType = Field(
        ...,
        title="MediaCreatedEvent.CreatedAt",
    )
    data: DataFieldType[MediaCreatedEventData] = Field(
        ...,
        title="MediaCreatedEvent.Data",
    )


class MediaUpdatedEventData(SerializableModel):
    """Data of a media updated event."""

    media: mm.Media = Field(
        ...,
        title="MediaUpdatedEventData.Media",
        description="Media that was updated.",
    )


class MediaUpdatedEvent(SerializableModel):
    """Event that is emitted when media is updated."""

    type: TypeFieldType[Literal["media-updated"]] = Field(
        "media-updated",
        title="MediaUpdatedEvent.Type",
    )
    created_at: CreatedAtFieldType = Field(
        ...,
        title="MediaUpdatedEvent.CreatedAt",
    )
    data: DataFieldType[MediaUpdatedEventData] = Field(
        ...,
        title="MediaUpdatedEvent.Data",
    )


class MediaDeletedEventData(SerializableModel):
    """Data of a media deleted event."""

    media: mm.Media = Field(
        ...,
        title="MediaDeletedEventData.Media",
        description="Media that was deleted.",
    )


class MediaDeletedEvent(SerializableModel):
    """Event that is emitted when media is deleted."""

    type: TypeFieldType[Literal["media-deleted"]] = Field(
        "media-deleted",
        title="MediaDeletedEvent.Type",
    )
    created_at: CreatedAtFieldType = Field(
        ...,
        title="MediaDeletedEvent.CreatedAt",
    )
    data: DataFieldType[MediaDeletedEventData] = Field(
        ...,
        title="MediaDeletedEvent.Data",
    )


Event = Annotated[
    MediaCreatedEvent | MediaUpdatedEvent | MediaDeletedEvent,
    Field(..., discriminator="type"),
]
ParsableEvent = RootModel[Event]
