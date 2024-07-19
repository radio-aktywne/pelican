from dataclasses import dataclass

from typing_extensions import TypedDict

from emitunes.datatunes import models as dm
from emitunes.datatunes import types as dt

Binding = dm.Binding

BindingWhereInput = dt.BindingWhereInput

BindingInclude = dt.BindingInclude

BindingWhereUniqueInput = dt.BindingWhereUniqueInput

BindingOrderByInput = dt.BindingOrderByInput


class BindingOptionalCreateInput(TypedDict, total=False):
    """Optional arguments to the Binding create method"""

    id: str


class BindingCreateInput(BindingOptionalCreateInput):
    """Required arguments to the Binding create method"""

    playlistId: str  # noqa: N815
    mediaId: str  # noqa: N815
    rank: str


BindingUpdateInput = dt.BindingUpdateManyMutationInput


@dataclass(kw_only=True)
class CountRequest:
    """Request to count bindings."""

    where: BindingWhereInput | None = None


@dataclass(kw_only=True)
class CountResponse:
    """Response for counting bindings."""

    count: int


@dataclass(kw_only=True)
class ListRequest:
    """Request to list bindings."""

    limit: int | None = None
    offset: int | None = None
    where: BindingWhereInput | None = None
    include: BindingInclude | None = None
    order: BindingOrderByInput | list[BindingOrderByInput] | None = None


@dataclass(kw_only=True)
class ListResponse:
    """Response for listing bindings."""

    bindings: list[Binding]


@dataclass(kw_only=True)
class GetRequest:
    """Request to get a binding."""

    where: BindingWhereUniqueInput
    include: BindingInclude | None = None


@dataclass(kw_only=True)
class GetResponse:
    """Response for getting a binding."""

    binding: Binding | None


@dataclass(kw_only=True)
class CreateRequest:
    """Request to create a binding."""

    data: BindingCreateInput
    include: BindingInclude | None = None


@dataclass(kw_only=True)
class CreateResponse:
    """Response for creating a binding."""

    binding: Binding


@dataclass(kw_only=True)
class UpdateRequest:
    """Request to update a binding."""

    data: BindingUpdateInput
    where: BindingWhereUniqueInput
    include: BindingInclude | None = None


@dataclass(kw_only=True)
class UpdateResponse:
    """Response for updating a binding."""

    binding: Binding | None


@dataclass(kw_only=True)
class DeleteRequest:
    """Request to delete a binding."""

    where: BindingWhereUniqueInput
    include: BindingInclude | None = None


@dataclass(kw_only=True)
class DeleteResponse:
    """Response for deleting a binding."""

    binding: Binding | None
