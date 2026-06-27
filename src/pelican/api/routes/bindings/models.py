from collections.abc import Sequence
from typing import Self
from uuid import UUID

from pelican.models.base import SerializableModel, datamodel
from pelican.services.entities.bindings import models as bm


class Playlist(SerializableModel):
    """Playlist data."""

    id: UUID
    """Identifier of the playlist."""

    name: str
    """Name of the playlist."""

    bindings: Sequence["Binding"] | None
    """Bindings the playlist belongs to."""

    @classmethod
    def map(cls, playlist: bm.Playlist) -> Self:
        """Map from internal representation."""
        return cls(
            id=UUID(playlist.id),
            name=playlist.name,
            bindings=(
                [Binding.map(binding) for binding in playlist.bindings]
                if playlist.bindings is not None
                else None
            ),
        )


class Media(SerializableModel):
    """Media data."""

    id: UUID
    """Identifier of the media."""

    name: str
    """Name of the media."""

    bindings: Sequence["Binding"] | None
    """Bindings the media belongs to."""

    @classmethod
    def map(cls, media: bm.Media) -> Self:
        """Map from internal representation."""
        return cls(
            id=UUID(media.id),
            name=media.name,
            bindings=(
                [Binding.map(binding) for binding in media.bindings]
                if media.bindings is not None
                else None
            ),
        )


class Binding(SerializableModel):
    """Binding data."""

    id: UUID
    """Identifier of the binding."""

    playlist_id: UUID
    """Identifier of the playlist the binding belongs to."""

    media_id: UUID
    """Identifier of the media the binding belongs to."""

    rank: str
    """Rank of the media in the binding."""

    playlist: Playlist | None
    """Playlist the binding belongs to."""

    media: Media | None
    """Media the binding belongs to."""

    @classmethod
    def map(cls, binding: bm.Binding) -> Self:
        """Map from internal representation."""
        return cls(
            id=UUID(binding.id),
            playlist_id=UUID(binding.playlistId),
            media_id=UUID(binding.mediaId),
            rank=binding.rank,
            playlist=Playlist.map(binding.playlist) if binding.playlist else None,
            media=Media.map(binding.media) if binding.media else None,
        )


class BindingList(SerializableModel):
    """List of bindings."""

    count: int
    """Total number of bindings that matched the query."""

    limit: int | None
    """Maximum number of returned bindings."""

    offset: int | None
    """Number of bindings skipped."""

    bindings: Sequence[Binding]
    """Bindings that matched the request."""


type ListRequestLimit = int | None

type ListRequestOffset = int | None

type ListRequestWhere = bm.BindingWhereInput | None

type ListRequestInclude = bm.BindingInclude | None

type ListRequestOrder = bm.BindingOrderByInput | Sequence[bm.BindingOrderByInput] | None

type ListResponseResults = BindingList

type GetRequestId = UUID

type GetRequestInclude = bm.BindingInclude | None

type GetResponseBinding = Binding

type CreateRequestData = bm.BindingCreateInput

type CreateRequestInclude = bm.BindingInclude | None

type CreateResponseBinding = Binding

type UpdateRequestData = bm.BindingUpdateInput

type UpdateRequestId = UUID

type UpdateRequestInclude = bm.BindingInclude | None

type UpdateResponseBinding = Binding

type DeleteRequestId = UUID


@datamodel
class ListRequest:
    """Request to list bindings."""

    limit: ListRequestLimit
    """Maximum number of bindings to return."""

    offset: ListRequestOffset
    """Number of bindings to skip."""

    where: ListRequestWhere
    """Filter to apply to find bindings."""

    include: ListRequestInclude
    """Relations to include in the response."""

    order: ListRequestOrder
    """Order to apply to the results."""


@datamodel
class ListResponse:
    """Response for listing bindings."""

    results: ListResponseResults
    """List of bindings."""


@datamodel
class GetRequest:
    """Request to get a binding."""

    id: GetRequestId
    """Identifier of the binding to get."""

    include: GetRequestInclude
    """Relations to include in the response."""


@datamodel
class GetResponse:
    """Response for getting a binding."""

    binding: GetResponseBinding
    """Binding that matched the request."""


@datamodel
class CreateRequest:
    """Request to create a binding."""

    data: CreateRequestData
    """Data to create a binding."""

    include: CreateRequestInclude
    """Relations to include in the response."""


@datamodel
class CreateResponse:
    """Response for creating a binding."""

    binding: CreateResponseBinding
    """Binding that was created."""


@datamodel
class UpdateRequest:
    """Request to update a binding."""

    data: UpdateRequestData
    """Data to update a binding."""

    id: UpdateRequestId
    """Identifier of the binding to update."""

    include: UpdateRequestInclude
    """Relations to include in the response."""


@datamodel
class UpdateResponse:
    """Response for updating a binding."""

    binding: UpdateResponseBinding
    """Binding that was updated."""


@datamodel
class DeleteRequest:
    """Request to delete a binding."""

    id: DeleteRequestId
    """Identifier of the binding to delete."""


@datamodel
class DeleteResponse:
    """Response for deleting a binding."""
