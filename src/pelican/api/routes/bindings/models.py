from uuid import UUID

from pelican.models.base import SerializableModel, datamodel, serializable
from pelican.services.bindings import models as bm


class Playlist(SerializableModel):
    """Playlist data."""

    id: UUID
    """Identifier of the playlist."""

    name: str
    """Name of the playlist."""

    bindings: list["Binding"] | None
    """Bindings that the playlist belongs to."""

    @staticmethod
    def map(playlist: bm.Playlist) -> "Playlist":
        return Playlist(
            id=playlist.id,
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

    bindings: list["Binding"] | None
    """Bindings that the media belongs to."""

    @staticmethod
    def map(media: bm.Media) -> "Media":
        return Media(
            id=media.id,
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
    """Identifier of the playlist that the binding belongs to."""

    media_id: UUID
    """Identifier of the media that the binding belongs to."""

    rank: str
    """Rank of the media in the binding."""

    playlist: Playlist | None
    """Playlist that the binding belongs to."""

    media: Media | None
    """Media that the binding belongs to."""

    @staticmethod
    def map(binding: bm.Binding) -> "Binding":
        return Binding(
            id=binding.id,
            playlist_id=binding.playlistId,
            media_id=binding.mediaId,
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

    bindings: list[Binding]
    """Bindings that matched the request."""


@serializable
class BindingWhereInput(bm.BindingWhereInput):
    pass


@serializable
class BindingWhereUniqueIdInput(bm.BindingWhereUniqueIdInput):
    pass


@serializable
class BindingWhereUniquePlaylistIdRankInput(bm.BindingWhereUniquePlaylistIdRankInput):
    pass


BindingWhereUniqueInput = (
    BindingWhereUniqueIdInput | BindingWhereUniquePlaylistIdRankInput
)


@serializable
class BindingInclude(bm.BindingInclude):
    pass


@serializable
class BindingOrderByIdInput(bm.BindingOrderByIdInput):
    pass


@serializable
class BindingOrderByPlaylistIdInput(bm.BindingOrderByPlaylistIdInput):
    pass


@serializable
class BindingOrderByMediaIdInput(bm.BindingOrderByMediaIdInput):
    pass


@serializable
class BindingOrderByRankInput(bm.BindingOrderByRankInput):
    pass


BindingOrderByInput = (
    BindingOrderByIdInput
    | BindingOrderByPlaylistIdInput
    | BindingOrderByMediaIdInput
    | BindingOrderByRankInput
)


@serializable
class BindingCreateInput(bm.BindingCreateInput):
    pass


@serializable
class BindingUpdateInput(bm.BindingUpdateInput):
    pass


ListRequestLimit = int | None

ListRequestOffset = int | None

ListRequestWhere = BindingWhereInput | None

ListRequestInclude = BindingInclude | None

ListRequestOrder = BindingOrderByInput | list[BindingOrderByInput] | None

ListResponseResults = BindingList

GetRequestId = UUID

GetRequestInclude = BindingInclude | None

GetResponseBinding = Binding

CreateRequestData = BindingCreateInput

CreateRequestInclude = BindingInclude | None

CreateResponseBinding = Binding

UpdateRequestData = BindingUpdateInput

UpdateRequestId = UUID

UpdateRequestInclude = BindingInclude | None

UpdateResponseBinding = Binding

DeleteRequestId = UUID


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

    pass
