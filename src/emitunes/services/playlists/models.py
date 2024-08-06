from emitunes.models.base import datamodel
from emitunes.services.datatunes import models as dm
from emitunes.services.datatunes import types as dt

Playlist = dm.Playlist

PlaylistWhereInput = dt.PlaylistWhereInput

PlaylistInclude = dt.PlaylistInclude

PlaylistWhereUniqueIdInput = dt._PlaylistWhereUnique_id_Input

PlaylistWhereUniqueNameInput = dt._PlaylistWhereUnique_name_Input

PlaylistWhereUniqueInput = PlaylistWhereUniqueIdInput | PlaylistWhereUniqueNameInput

PlaylistOrderByIdInput = dt._Playlist_id_OrderByInput

PlaylistOrderByNameInput = dt._Playlist_name_OrderByInput

PlaylistOrderByInput = PlaylistOrderByIdInput | PlaylistOrderByNameInput

PlaylistCreateInput = dt.PlaylistCreateWithoutRelationsInput

PlaylistUpdateInput = dt.PlaylistUpdateManyMutationInput


@datamodel
class CountRequest:
    """Request to count playlists."""

    where: PlaylistWhereInput | None
    """Filter to apply to find playlists."""


@datamodel
class CountResponse:
    """Response for counting playlists."""

    count: int
    """Number of playlists that match the filter."""


@datamodel
class ListRequest:
    """Request to list playlists."""

    limit: int | None
    """Maximum number of playlists to return."""

    offset: int | None
    """Number of playlists to skip."""

    where: PlaylistWhereInput | None
    """Filter to apply to find playlists."""

    include: PlaylistInclude | None
    """Relations to include in the response."""

    order: PlaylistOrderByInput | list[PlaylistOrderByInput] | None
    """Order to apply to the results."""


@datamodel
class ListResponse:
    """Response for listing playlists."""

    playlists: list[Playlist]
    """List of playlists that match the filter."""


@datamodel
class GetRequest:
    """Request to get a playlist."""

    where: PlaylistWhereUniqueInput
    """Unique filter to apply to find a playlist."""

    include: PlaylistInclude | None
    """Relations to include in the response."""


@datamodel
class GetResponse:
    """Response for getting a playlist."""

    playlist: Playlist | None
    """Playlist that matches the filter."""


@datamodel
class CreateRequest:
    """Request to create a playlist."""

    data: PlaylistCreateInput
    """Data to create a playlist."""

    include: PlaylistInclude | None
    """Relations to include in the response."""


@datamodel
class CreateResponse:
    """Response for creating a playlist."""

    playlist: Playlist
    """Playlist that was created."""


@datamodel
class UpdateRequest:
    """Request to update a playlist."""

    data: PlaylistUpdateInput
    """Data to update a playlist."""

    where: PlaylistWhereUniqueInput
    """Unique filter to apply to find a playlist."""

    include: PlaylistInclude | None
    """Relations to include in the response."""


@datamodel
class UpdateResponse:
    """Response for updating a playlist."""

    playlist: Playlist | None
    """Playlist that was updated."""


@datamodel
class DeleteRequest:
    """Request to delete a playlist."""

    where: PlaylistWhereUniqueInput
    """Unique filter to apply to find a playlist."""

    include: PlaylistInclude | None
    """Relations to include in the response."""


@datamodel
class DeleteResponse:
    """Response for deleting a playlist."""

    playlist: Playlist | None
    """Playlist that was deleted."""


@datamodel
class M3URequest:
    """Request to get the playlist in M3U format."""

    where: PlaylistWhereUniqueInput
    """Unique filter to apply to find a playlist."""

    base: str
    """Base URL of the service."""


@datamodel
class M3UResponse:
    """Response for getting the playlist in M3U format."""

    m3u: str | None
    """Playlist in M3U format."""
