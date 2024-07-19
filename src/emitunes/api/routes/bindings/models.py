from dataclasses import dataclass
from uuid import UUID

from pydantic import Field

from emitunes.bindings import models as pm
from emitunes.models.base import SerializableModel

ListRequestLimit = int | None

ListRequestOffset = int | None

ListRequestWhere = pm.BindingWhereInput | None

ListRequestInclude = pm.BindingInclude | None

ListRequestOrder = pm.BindingOrderByInput | list[pm.BindingOrderByInput] | None

GetRequestId = UUID

GetRequestInclude = pm.BindingInclude | None

GetResponseBinding = pm.Binding

CreateRequestData = pm.BindingCreateInput

CreateRequestInclude = pm.BindingInclude | None

CreateResponseBinding = pm.Binding

UpdateRequestData = pm.BindingUpdateInput

UpdateRequestId = UUID

UpdateRequestInclude = pm.BindingInclude | None

UpdateResponseBinding = pm.Binding

DeleteRequestId = UUID


class ListResponseResults(SerializableModel):
    """Results of a list request."""

    count: int = Field(
        ...,
        title="ListResponseResults.Count",
        description="Total number of bindings that matched the query.",
    )
    limit: int | None = Field(
        ...,
        title="ListResponseResults.Limit",
        description="Maximum number of returned bindings.",
    )
    offset: int | None = Field(
        ...,
        title="ListResponseResults.Offset",
        description="Number of bindings skipped.",
    )
    bindings: list[pm.Binding] = Field(
        ...,
        title="ListResponseResults.Bindings",
        description="Bindings that matched the request.",
    )


@dataclass(kw_only=True)
class ListRequest:
    """Request to list bindings."""

    limit: ListRequestLimit
    offset: ListRequestOffset
    where: ListRequestWhere
    include: ListRequestInclude
    order: ListRequestOrder


@dataclass(kw_only=True)
class ListResponse:
    """Response for listing bindings."""

    results: ListResponseResults


@dataclass(kw_only=True)
class GetRequest:
    """Request to get a binding."""

    id: GetRequestId
    include: GetRequestInclude


@dataclass(kw_only=True)
class GetResponse:
    """Response for getting a binding."""

    binding: GetResponseBinding


@dataclass(kw_only=True)
class CreateRequest:
    """Request to create a binding."""

    data: CreateRequestData
    include: CreateRequestInclude


@dataclass(kw_only=True)
class CreateResponse:
    """Response for creating a binding."""

    binding: CreateResponseBinding


@dataclass(kw_only=True)
class UpdateRequest:
    """Request to update a binding."""

    data: UpdateRequestData
    id: UpdateRequestId
    include: UpdateRequestInclude


@dataclass(kw_only=True)
class UpdateResponse:
    """Response for updating a binding."""

    binding: UpdateResponseBinding


@dataclass(kw_only=True)
class DeleteRequest:
    """Request to delete a binding."""

    id: DeleteRequestId


@dataclass(kw_only=True)
class DeleteResponse:
    """Response for deleting a binding."""

    pass
