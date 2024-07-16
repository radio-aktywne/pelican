from dataclasses import dataclass
from uuid import UUID

from pydantic import Field

from emitunes.media import models as mm
from emitunes.models.base import SerializableModel

ListRequestLimit = int | None

ListRequestOffset = int | None

ListRequestWhere = mm.MediaWhereInput | None

ListRequestInclude = mm.MediaInclude | None

ListRequestOrder = mm.MediaOrderByInput | list[mm.MediaOrderByInput] | None

GetRequestId = UUID

GetRequestInclude = mm.MediaInclude | None

GetResponseMedia = mm.Media

CreateRequestData = mm.MediaCreateInput

CreateRequestInclude = mm.MediaInclude | None

CreateResponseMedia = mm.Media

UpdateRequestData = mm.MediaUpdateInput

UpdateRequestId = UUID

UpdateRequestInclude = mm.MediaInclude | None

UpdateResponseMedia = mm.Media

DeleteRequestId = UUID

UploadRequestId = UUID

UploadRequestContent = mm.UploadContent

DownloadRequestId = UUID

DownloadResponseMedia = mm.Media

DownloadResponseContent = mm.DownloadContent


class ListResponseResults(SerializableModel):
    """Results of a list request."""

    count: int = Field(
        ...,
        title="ListResponseResults.Count",
        description="Total number of media that matched the query.",
    )
    limit: int | None = Field(
        ...,
        title="ListResponseResults.Limit",
        description="Maximum number of returned media.",
    )
    offset: int | None = Field(
        ...,
        title="ListResponseResults.Offset",
        description="Number of media skipped.",
    )
    media: list[mm.Media] = Field(
        ...,
        title="ListResponseResults.Media",
        description="Media that matched the request.",
    )


@dataclass(kw_only=True)
class ListRequest:
    """Request to list media."""

    limit: ListRequestLimit
    offset: ListRequestOffset
    where: ListRequestWhere
    include: ListRequestInclude
    order: ListRequestOrder


@dataclass(kw_only=True)
class ListResponse:
    """Response for listing media."""

    results: ListResponseResults


@dataclass(kw_only=True)
class GetRequest:
    """Request to get media."""

    id: GetRequestId
    include: GetRequestInclude


@dataclass(kw_only=True)
class GetResponse:
    """Response for getting media."""

    media: GetResponseMedia


@dataclass(kw_only=True)
class CreateRequest:
    """Request to create media."""

    data: CreateRequestData
    include: CreateRequestInclude


@dataclass(kw_only=True)
class CreateResponse:
    """Response for creating media."""

    media: CreateResponseMedia


@dataclass(kw_only=True)
class UpdateRequest:
    """Request to update media."""

    data: UpdateRequestData
    id: UpdateRequestId
    include: UpdateRequestInclude


@dataclass(kw_only=True)
class UpdateResponse:
    """Response for updating media."""

    media: UpdateResponseMedia


@dataclass(kw_only=True)
class DeleteRequest:
    """Request to delete media."""

    id: DeleteRequestId


@dataclass(kw_only=True)
class DeleteResponse:
    """Response for deleting media."""

    pass


@dataclass(kw_only=True)
class UploadRequest:
    """Request to upload media content."""

    id: UploadRequestId
    content: UploadRequestContent


@dataclass(kw_only=True)
class UploadResponse:
    """Response for uploading media content."""

    pass


@dataclass(kw_only=True)
class DownloadRequest:
    """Request to download media content."""

    id: DownloadRequestId


@dataclass(kw_only=True)
class DownloadResponse:
    """Response for downloading media content."""

    content: DownloadResponseContent
