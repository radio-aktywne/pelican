from typing import Literal, Self
from uuid import UUID

from pydantic import Field

from pelican.models.base import SerializableModel
from pelican.models.events import types as t
from pelican.services.bindings import models as bm
from pelican.utils.time import naiveutcnow


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

    @classmethod
    def map(cls, binding: bm.Binding) -> Self:
        """Map to internal representation."""
        return cls(
            id=UUID(binding.id),
            playlist_id=UUID(binding.playlistId),
            media_id=UUID(binding.mediaId),
            rank=binding.rank,
        )


class BindingCreatedEventData(SerializableModel):
    """Data of a binding created event."""

    binding: Binding
    """Binding that was created."""


class BindingCreatedEvent(SerializableModel):
    """Event that is emitted when binding is created."""

    type: t.TypeField[Literal["binding-created"]] = "binding-created"
    created_at: t.CreatedAtField = Field(default_factory=naiveutcnow)
    data: t.DataField[BindingCreatedEventData]


class BindingUpdatedEventData(SerializableModel):
    """Data of a binding updated event."""

    binding: Binding
    """Binding that was updated."""


class BindingUpdatedEvent(SerializableModel):
    """Event that is emitted when binding is updated."""

    type: t.TypeField[Literal["binding-updated"]] = "binding-updated"
    created_at: t.CreatedAtField = Field(default_factory=naiveutcnow)
    data: t.DataField[BindingUpdatedEventData]


class BindingDeletedEventData(SerializableModel):
    """Data of a binding deleted event."""

    binding: Binding
    """Binding that was deleted."""


class BindingDeletedEvent(SerializableModel):
    """Event that is emitted when binding is deleted."""

    type: t.TypeField[Literal["binding-deleted"]] = "binding-deleted"
    created_at: t.CreatedAtField = Field(default_factory=naiveutcnow)
    data: t.DataField[BindingDeletedEventData]
