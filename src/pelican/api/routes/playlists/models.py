from collections.abc import Sequence
from typing import Self
from uuid import UUID

from pelican.models.base import SerializableModel, datamodel
from pelican.services.playlists import models as pm


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

    @classmethod
    def map(cls, binding: pm.Binding) -> Self:
        """Map to internal representation."""
        return cls(
            id=UUID(binding.id),
            playlist_id=UUID(binding.playlistId),
            media_id=UUID(binding.mediaId),
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

    bindings: Sequence[Binding] | None
    """Bindings that the media belongs to."""

    @classmethod
    def map(cls, media: pm.Media) -> Self:
        """Map to internal representation."""
        return cls(
            id=UUID(media.id),
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

    bindings: Sequence[Binding] | None
    """Bindings that the playlist belongs to."""

    @classmethod
    def map(cls, playlist: pm.Playlist) -> Self:
        """Map to internal representation."""
        return cls(
            id=UUID(playlist.id),
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

    playlists: Sequence[Playlist]
    """Playlists that matched the request."""


PlaylistWhereInput = pm.PlaylistWhereInput

PlaylistWhereUniqueIdInput = pm.PlaylistWhereUniqueIdInput

PlaylistWhereUniqueNameInput = pm.PlaylistWhereUniqueNameInput

type PlaylistWhereUniqueInput = (
    PlaylistWhereUniqueIdInput | PlaylistWhereUniqueNameInput
)

PlaylistInclude = pm.PlaylistInclude

PlaylistOrderByIdInput = pm.PlaylistOrderByIdInput

PlaylistOrderByNameInput = pm.PlaylistOrderByNameInput

type PlaylistOrderByInput = PlaylistOrderByIdInput | PlaylistOrderByNameInput

PlaylistCreateInput = pm.PlaylistCreateInput

PlaylistUpdateInput = pm.PlaylistUpdateInput

type ListRequestLimit = int | None

type ListRequestOffset = int | None

type ListRequestWhere = PlaylistWhereInput | None

type ListRequestInclude = PlaylistInclude | None

type ListRequestOrder = PlaylistOrderByInput | Sequence[PlaylistOrderByInput] | None

type ListResponseResults = PlaylistList

type GetRequestId = UUID

type GetRequestInclude = PlaylistInclude | None

type GetResponsePlaylist = Playlist

type CreateRequestData = PlaylistCreateInput

type CreateRequestInclude = PlaylistInclude | None

type CreateResponsePlaylist = Playlist

type UpdateRequestData = PlaylistUpdateInput

type UpdateRequestId = UUID

type UpdateRequestInclude = PlaylistInclude | None

type UpdateResponsePlaylist = Playlist

type DeleteRequestId = UUID

type M3URequestId = UUID

type M3URequestBase = str

type M3UResponseM3U = str

type HeadM3URequestId = UUID

type HeadM3URequestBase = str

type HeadM3UResponseM3U = str


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
