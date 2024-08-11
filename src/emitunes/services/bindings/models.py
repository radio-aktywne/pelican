from typing import TypedDict

from emitunes.models.base import datamodel
from emitunes.services.datatunes import models as dm
from emitunes.services.datatunes import types as dt

Media = dm.Media

Playlist = dm.Playlist

Binding = dm.Binding

BindingWhereInput = dt.BindingWhereInput

BindingInclude = dt.BindingInclude

BindingWhereUniqueIdInput = dt._BindingWhereUnique_id_Input

BindingWhereUniquePlaylistIdRankInput = dt._BindingCompoundplaylistId_rankKey

BindingWhereUniqueInput = (
    BindingWhereUniqueIdInput | BindingWhereUniquePlaylistIdRankInput
)

BindingOrderByIdInput = dt._Binding_id_OrderByInput

BindingOrderByPlaylistIdInput = dt._Binding_playlistId_OrderByInput

BindingOrderByMediaIdInput = dt._Binding_mediaId_OrderByInput

BindingOrderByRankInput = dt._Binding_rank_OrderByInput

BindingOrderByInput = (
    BindingOrderByIdInput
    | BindingOrderByPlaylistIdInput
    | BindingOrderByMediaIdInput
    | BindingOrderByRankInput
)


class BindingOptionalCreateInput(TypedDict, total=False):
    """Optional arguments to the Binding create method"""

    id: str


class BindingCreateInput(BindingOptionalCreateInput):
    """Required arguments to the Binding create method"""

    playlistId: str  # noqa: N815
    mediaId: str  # noqa: N815
    rank: str


BindingUpdateInput = dt.BindingUpdateManyMutationInput


@datamodel
class CountRequest:
    """Request to count bindings."""

    where: BindingWhereInput | None
    """Filter to apply to find bindings."""


@datamodel
class CountResponse:
    """Response for counting bindings."""

    count: int
    """Number of bindings that match the filter."""


@datamodel
class ListRequest:
    """Request to list bindings."""

    limit: int | None
    """Maximum number of bindings to return."""

    offset: int | None
    """Number of bindings to skip."""

    where: BindingWhereInput | None
    """Filter to apply to find bindings."""

    include: BindingInclude | None
    """Relations to include in the response."""

    order: BindingOrderByInput | list[BindingOrderByInput] | None
    """Order to apply to the results."""


@datamodel
class ListResponse:
    """Response for listing bindings."""

    bindings: list[Binding]
    """List of bindings that match the filter."""


@datamodel
class GetRequest:
    """Request to get a binding."""

    where: BindingWhereUniqueInput
    """Unique filter to apply to find a binding."""

    include: BindingInclude | None
    """Relations to include in the response."""


@datamodel
class GetResponse:
    """Response for getting a binding."""

    binding: Binding | None
    """Binding that matches the filter."""


@datamodel
class CreateRequest:
    """Request to create a binding."""

    data: BindingCreateInput
    """Data to create a binding."""

    include: BindingInclude | None
    """Relations to include in the response."""


@datamodel
class CreateResponse:
    """Response for creating a binding."""

    binding: Binding
    """Created binding."""


@datamodel
class UpdateRequest:
    """Request to update a binding."""

    data: BindingUpdateInput
    """Data to update a binding."""

    where: BindingWhereUniqueInput
    """Unique filter to apply to find a binding."""

    include: BindingInclude | None
    """Relations to include in the response."""


@datamodel
class UpdateResponse:
    """Response for updating a binding."""

    binding: Binding | None
    """Binding that was updated."""


@datamodel
class DeleteRequest:
    """Request to delete a binding."""

    where: BindingWhereUniqueInput
    """Unique filter to apply to find a binding."""

    include: BindingInclude | None
    """Relations to include in the response."""


@datamodel
class DeleteResponse:
    """Response for deleting a binding."""

    binding: Binding | None
    """Binding that was deleted."""
