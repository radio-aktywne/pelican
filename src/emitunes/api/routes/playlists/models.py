from dataclasses import dataclass
from uuid import UUID

from pydantic import Field

from emitunes.models.base import SerializableModel
from emitunes.playlists import models as pm

ListRequestLimit = int | None

ListRequestOffset = int | None

ListRequestWhere = pm.PlaylistWhereInput | None

ListRequestInclude = pm.PlaylistInclude | None

ListRequestOrder = pm.PlaylistOrderByInput | list[pm.PlaylistOrderByInput] | None

GetRequestId = UUID

GetRequestInclude = pm.PlaylistInclude | None

GetResponsePlaylist = pm.Playlist

CreateRequestData = pm.PlaylistCreateInput

CreateRequestInclude = pm.PlaylistInclude | None

CreateResponsePlaylist = pm.Playlist

UpdateRequestData = pm.PlaylistUpdateInput

UpdateRequestId = UUID

UpdateRequestInclude = pm.PlaylistInclude | None

UpdateResponsePlaylist = pm.Playlist

DeleteRequestId = UUID

M3URequestId = UUID

M3URequestBase = str

M3UResponseM3U = str


class ListResponseResults(SerializableModel):
    """Results of a list request."""

    count: int = Field(
        ...,
        title="ListResponseResults.Count",
        description="Total number of playlists that matched the query.",
    )
    limit: int | None = Field(
        ...,
        title="ListResponseResults.Limit",
        description="Maximum number of returned playlists.",
    )
    offset: int | None = Field(
        ...,
        title="ListResponseResults.Offset",
        description="Number of playlists skipped.",
    )
    playlists: list[pm.Playlist] = Field(
        ...,
        title="ListResponseResults.Playlists",
        description="Playlists that matched the request.",
    )


@dataclass(kw_only=True)
class ListRequest:
    """Request to list playlists."""

    limit: ListRequestLimit
    offset: ListRequestOffset
    where: ListRequestWhere
    include: ListRequestInclude
    order: ListRequestOrder


@dataclass(kw_only=True)
class ListResponse:
    """Response for listing playlists."""

    results: ListResponseResults


@dataclass(kw_only=True)
class GetRequest:
    """Request to get a playlist."""

    id: GetRequestId
    include: GetRequestInclude


@dataclass(kw_only=True)
class GetResponse:
    """Response for getting a playlist."""

    playlist: GetResponsePlaylist


@dataclass(kw_only=True)
class CreateRequest:
    """Request to create a playlist."""

    data: CreateRequestData
    include: CreateRequestInclude


@dataclass(kw_only=True)
class CreateResponse:
    """Response for creating a playlist."""

    playlist: CreateResponsePlaylist


@dataclass(kw_only=True)
class UpdateRequest:
    """Request to update a playlist."""

    data: UpdateRequestData
    id: UpdateRequestId
    include: UpdateRequestInclude


@dataclass(kw_only=True)
class UpdateResponse:
    """Response for updating a playlist."""

    playlist: UpdateResponsePlaylist


@dataclass(kw_only=True)
class DeleteRequest:
    """Request to delete a playlist."""

    id: DeleteRequestId


@dataclass(kw_only=True)
class DeleteResponse:
    """Response for deleting a playlist."""

    pass


@dataclass(kw_only=True)
class M3URequest:
    """Request to get a playlist in M3U format."""

    id: M3URequestId
    base: M3URequestBase


@dataclass(kw_only=True)
class M3UResponse:
    """Response for getting a playlist in M3U format."""

    m3u: M3UResponseM3U
