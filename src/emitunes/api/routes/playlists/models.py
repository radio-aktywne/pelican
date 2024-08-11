from uuid import UUID

from emitunes.models.base import SerializableModel, datamodel, serializable
from emitunes.services.playlists import models as pm


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

    playlist: "Playlist | None"
    """Playlist that the binding belongs to."""

    media: "Media | None"
    """Media that the binding belongs to."""

    @staticmethod
    def map(binding: pm.Binding) -> "Binding":
        return Binding(
            id=binding.id,
            playlist_id=binding.playlistId,
            media_id=binding.mediaId,
            rank=binding.rank,
            playlist=Playlist.map(binding.playlist) if binding.playlist else None,
            media=Media.map(binding.media) if binding.media else None,
        )


class Media(SerializableModel):
    """Media data."""

    id: UUID
    """Identifier of the media."""

    name: str
    """Name of the media."""

    bindings: list[Binding] | None
    """Bindings that the media belongs to."""

    @staticmethod
    def map(media: pm.Media) -> "Media":
        return Media(
            id=media.id,
            name=media.name,
            bindings=(
                [Binding.map(binding) for binding in media.bindings]
                if media.bindings is not None
                else None
            ),
        )


class Playlist(SerializableModel):
    """Playlist data."""

    id: UUID
    """Identifier of the playlist."""

    name: str
    """Name of the playlist."""

    bindings: list[Binding] | None
    """Bindings that the playlist belongs to."""

    @staticmethod
    def map(playlist: pm.Playlist) -> "Playlist":
        return Playlist(
            id=playlist.id,
            name=playlist.name,
            bindings=(
                [Binding.map(binding) for binding in playlist.bindings]
                if playlist.bindings is not None
                else None
            ),
        )


class PlaylistList(SerializableModel):
    """List of playlists."""

    count: int
    """Total number of playlists that matched the query."""

    limit: int | None
    """Maximum number of returned playlists."""

    offset: int | None
    """Number of playlists skipped."""

    playlists: list[Playlist]
    """Playlists that matched the request."""


@serializable
class PlaylistWhereInput(pm.PlaylistWhereInput):
    pass


@serializable
class PlaylistWhereUniqueIdInput(pm.PlaylistWhereUniqueIdInput):
    pass


@serializable
class PlaylistWhereUniqueNameInput(pm.PlaylistWhereUniqueNameInput):
    pass


PlaylistWhereUniqueInput = PlaylistWhereUniqueIdInput | PlaylistWhereUniqueNameInput


@serializable
class PlaylistInclude(pm.PlaylistInclude):
    pass


@serializable
class PlaylistOrderByIdInput(pm.PlaylistOrderByIdInput):
    pass


@serializable
class PlaylistOrderByNameInput(pm.PlaylistOrderByNameInput):
    pass


PlaylistOrderByInput = PlaylistOrderByIdInput | PlaylistOrderByNameInput


@serializable
class PlaylistCreateInput(pm.PlaylistCreateInput):
    pass


@serializable
class PlaylistUpdateInput(pm.PlaylistUpdateInput):
    pass


ListRequestLimit = int | None

ListRequestOffset = int | None

ListRequestWhere = PlaylistWhereInput | None

ListRequestInclude = PlaylistInclude | None

ListRequestOrder = PlaylistOrderByInput | list[PlaylistOrderByInput] | None

ListResponseResults = PlaylistList

GetRequestId = UUID

GetRequestInclude = PlaylistInclude | None

GetResponsePlaylist = Playlist

CreateRequestData = PlaylistCreateInput

CreateRequestInclude = PlaylistInclude | None

CreateResponsePlaylist = Playlist

UpdateRequestData = PlaylistUpdateInput

UpdateRequestId = UUID

UpdateRequestInclude = PlaylistInclude | None

UpdateResponsePlaylist = Playlist

DeleteRequestId = UUID

M3URequestId = UUID

M3URequestBase = str

M3UResponseM3U = str

HeadM3URequestId = UUID

HeadM3URequestBase = str

HeadM3UResponseM3U = str


@datamodel
class ListRequest:
    """Request to list playlists."""

    limit: ListRequestLimit
    """Maximum number of playlists to return."""

    offset: ListRequestOffset
    """Number of playlists to skip."""

    where: ListRequestWhere
    """Filter to apply to find playlists."""

    include: ListRequestInclude
    """Relations to include in the response."""

    order: ListRequestOrder
    """Order to apply to the results."""


@datamodel
class ListResponse:
    """Response for listing playlists."""

    results: ListResponseResults
    """List of playlists."""


@datamodel
class GetRequest:
    """Request to get a playlist."""

    id: GetRequestId
    """Identifier of the playlist to get."""

    include: GetRequestInclude
    """Relations to include in the response."""


@datamodel
class GetResponse:
    """Response for getting a playlist."""

    playlist: GetResponsePlaylist
    """Playlist that matched the request."""


@datamodel
class CreateRequest:
    """Request to create a playlist."""

    data: CreateRequestData
    """Data to create a playlist."""

    include: CreateRequestInclude
    """Relations to include in the response."""


@datamodel
class CreateResponse:
    """Response for creating a playlist."""

    playlist: CreateResponsePlaylist
    """Playlist that was created."""


@datamodel
class UpdateRequest:
    """Request to update a playlist."""

    data: UpdateRequestData
    """Data to update a playlist."""

    id: UpdateRequestId
    """Identifier of the playlist to update."""

    include: UpdateRequestInclude
    """Relations to include in the response."""


@datamodel
class UpdateResponse:
    """Response for updating a playlist."""

    playlist: UpdateResponsePlaylist
    """Playlist that was updated."""


@datamodel
class DeleteRequest:
    """Request to delete a playlist."""

    id: DeleteRequestId
    """Identifier of the playlist to delete."""


@datamodel
class DeleteResponse:
    """Response for deleting a playlist."""

    pass


@datamodel
class M3URequest:
    """Request to get a playlist in M3U format."""

    id: M3URequestId
    """Identifier of the playlist to get."""

    base: M3URequestBase
    """Base URL of the service."""


@datamodel
class M3UResponse:
    """Response for getting a playlist in M3U format."""

    m3u: M3UResponseM3U
    """Playlist in M3U format."""


@datamodel
class HeadM3URequest:
    """Request to get headers for a playlist in M3U format."""

    id: HeadM3URequestId
    """Identifier of the playlist to get."""

    base: HeadM3URequestBase
    """Base URL of the service."""


@datamodel
class HeadM3UResponse:
    """Response for getting headers for a playlist in M3U format."""

    m3u: HeadM3UResponseM3U
