from dataclasses import dataclass

from emitunes.datatunes import models as dm
from emitunes.datatunes import types as dt

Playlist = dm.Playlist

PlaylistWhereInput = dt.PlaylistWhereInput

PlaylistInclude = dt.PlaylistInclude

PlaylistWhereUniqueInput = dt.PlaylistWhereUniqueInput

PlaylistOrderByInput = dt.PlaylistOrderByInput

PlaylistCreateInput = dt.PlaylistCreateWithoutRelationsInput

PlaylistUpdateInput = dt.PlaylistUpdateManyMutationInput


@dataclass(kw_only=True)
class CountRequest:
    """Request to count playlists."""

    where: PlaylistWhereInput | None = None


@dataclass(kw_only=True)
class CountResponse:
    """Response for counting playlists."""

    count: int


@dataclass(kw_only=True)
class ListRequest:
    """Request to list playlists."""

    limit: int | None = None
    offset: int | None = None
    where: PlaylistWhereInput | None = None
    include: PlaylistInclude | None = None
    order: PlaylistOrderByInput | list[PlaylistOrderByInput] | None = None


@dataclass(kw_only=True)
class ListResponse:
    """Response for listing playlists."""

    playlists: list[Playlist]


@dataclass(kw_only=True)
class GetRequest:
    """Request to get a playlist."""

    where: PlaylistWhereUniqueInput
    include: PlaylistInclude | None = None


@dataclass(kw_only=True)
class GetResponse:
    """Response for getting a playlist."""

    playlist: Playlist | None


@dataclass(kw_only=True)
class CreateRequest:
    """Request to create a playlist."""

    data: PlaylistCreateInput
    include: PlaylistInclude | None = None


@dataclass(kw_only=True)
class CreateResponse:
    """Response for creating a playlist."""

    playlist: Playlist


@dataclass(kw_only=True)
class UpdateRequest:
    """Request to update a playlist."""

    data: PlaylistUpdateInput
    where: PlaylistWhereUniqueInput
    include: PlaylistInclude | None = None


@dataclass(kw_only=True)
class UpdateResponse:
    """Response for updating a playlist."""

    playlist: Playlist | None


@dataclass(kw_only=True)
class DeleteRequest:
    """Request to delete a playlist."""

    where: PlaylistWhereUniqueInput
    include: PlaylistInclude | None = None


@dataclass(kw_only=True)
class DeleteResponse:
    """Response for deleting a playlist."""

    playlist: Playlist | None
