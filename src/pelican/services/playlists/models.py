from collections.abc import Sequence

from pelican.models.base import datamodel
from pelican.services.graphite import models as gm
from pelican.services.graphite import types as gt

Binding = gm.Binding

Media = gm.Media

Playlist = gm.Playlist

PlaylistWhereInput = gt.PlaylistWhereInput

PlaylistInclude = gt.PlaylistInclude

PlaylistWhereUniqueIdInput = gt._PlaylistWhereUnique_id_Input  # noqa: SLF001

PlaylistWhereUniqueNameInput = gt._PlaylistWhereUnique_name_Input  # noqa: SLF001

type PlaylistWhereUniqueInput = (
    PlaylistWhereUniqueIdInput | PlaylistWhereUniqueNameInput
)

PlaylistOrderByIdInput = gt._Playlist_id_OrderByInput  # noqa: SLF001

PlaylistOrderByNameInput = gt._Playlist_name_OrderByInput  # noqa: SLF001

type PlaylistOrderByInput = PlaylistOrderByIdInput | PlaylistOrderByNameInput

PlaylistCreateInput = gt.PlaylistCreateWithoutRelationsInput

PlaylistUpdateInput = gt.PlaylistUpdateManyMutationInput


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

    order: PlaylistOrderByInput | Sequence[PlaylistOrderByInput] | None
    """Order to apply to the results."""


@datamodel
class ListResponse:
    """Response for listing playlists."""

    playlists: Sequence[Playlist]
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
