from typing import Literal
from uuid import UUID

from emitunes.models.base import SerializableModel
from emitunes.models.events import types as t
from emitunes.services.bindings import models as bm


class Binding(SerializableModel):
    """Binding data."""

    id: UUID
    """Identifier of the binding."""

    playlist_id: UUID
    """Identifier of the playlist that the binding belongs to."""

    media_id: UUID
    """Identifier of the media that the binding belongs to."""

    rank: str
    """Rank of the media in the binding."""

    @staticmethod
    def map(binding: bm.Binding) -> "Binding":
        return Binding(
            id=binding.id,
            playlist_id=binding.playlistId,
            media_id=binding.mediaId,
            rank=binding.rank,
        )


class BindingCreatedEventData(SerializableModel):
    """Data of a binding created event."""

    binding: Binding
    """Binding that was created."""


class BindingCreatedEvent(SerializableModel):
    """Event that is emitted when binding is created."""

    type: t.TypeFieldType[Literal["binding-created"]] = "binding-created"
    created_at: t.CreatedAtFieldType
    data: t.DataFieldType[BindingCreatedEventData]


class BindingUpdatedEventData(SerializableModel):
    """Data of a binding updated event."""

    binding: Binding
    """Binding that was updated."""


class BindingUpdatedEvent(SerializableModel):
    """Event that is emitted when binding is updated."""

    type: t.TypeFieldType[Literal["binding-updated"]] = "binding-updated"
    created_at: t.CreatedAtFieldType
    data: t.DataFieldType[BindingUpdatedEventData]


class BindingDeletedEventData(SerializableModel):
    """Data of a binding deleted event."""

    binding: Binding
    """Binding that was deleted."""


class BindingDeletedEvent(SerializableModel):
    """Event that is emitted when binding is deleted."""

    type: t.TypeFieldType[Literal["binding-deleted"]] = "binding-deleted"
    created_at: t.CreatedAtFieldType
    data: t.DataFieldType[BindingDeletedEventData]
