from dataclasses import dataclass

from emitunes.datatunes import models as dm
from emitunes.datatunes import types as dt
from emitunes.mediatunes import models as mm

# Monkey-patching to simplify types
dt.MediaWhereUniqueInput = (
    dt._MediaWhereUnique_id_Input | dt._MediaWhereUnique_name_Input
)
dt.MediaOrderByInput = dt._Media_id_OrderByInput | dt._Media_name_OrderByInput

Media = dm.Media

MediaWhereInput = dt.MediaWhereInput

MediaInclude = dt.MediaInclude

MediaWhereUniqueInput = dt.MediaWhereUniqueInput

MediaOrderByInput = dt.MediaOrderByInput

MediaCreateInput = dt.MediaCreateInput

MediaUpdateInput = dt.MediaUpdateInput

UploadContent = mm.UploadContent

DownloadContent = mm.DownloadContent


@dataclass(kw_only=True)
class CountRequest:
    """Request to count media."""

    where: MediaWhereInput | None = None


@dataclass(kw_only=True)
class CountResponse:
    """Response for counting media."""

    count: int


@dataclass(kw_only=True)
class ListRequest:
    """Request to list media."""

    limit: int | None = None
    offset: int | None = None
    where: MediaWhereInput | None = None
    include: MediaInclude | None = None
    order: MediaOrderByInput | list[MediaOrderByInput] | None = None


@dataclass(kw_only=True)
class ListResponse:
    """Response for listing media."""

    media: list[Media]


@dataclass(kw_only=True)
class GetRequest:
    """Request to get media."""

    where: MediaWhereUniqueInput
    include: MediaInclude | None = None


@dataclass(kw_only=True)
class GetResponse:
    """Response for getting media."""

    media: Media | None


@dataclass(kw_only=True)
class CreateRequest:
    """Request to create media."""

    data: MediaCreateInput
    include: MediaInclude | None = None


@dataclass(kw_only=True)
class CreateResponse:
    """Response for creating media."""

    media: Media


@dataclass(kw_only=True)
class UpdateRequest:
    """Request to update media."""

    data: MediaUpdateInput
    where: MediaWhereUniqueInput
    include: MediaInclude | None = None


@dataclass(kw_only=True)
class UpdateResponse:
    """Response for updating media."""

    media: Media | None


@dataclass(kw_only=True)
class DeleteRequest:
    """Request to delete media."""

    where: MediaWhereUniqueInput
    include: MediaInclude | None = None


@dataclass(kw_only=True)
class DeleteResponse:
    """Response for deleting media."""

    media: Media | None


@dataclass(kw_only=True)
class UploadRequest:
    """Request to upload media content."""

    where: MediaWhereUniqueInput
    include: MediaInclude | None = None
    content: UploadContent


@dataclass(kw_only=True)
class UploadResponse:
    """Response for uploading media content."""

    media: Media | None


@dataclass(kw_only=True)
class DownloadRequest:
    """Request to download media content."""

    where: MediaWhereUniqueInput
    include: MediaInclude | None = None


@dataclass(kw_only=True)
class DownloadResponse:
    """Response for downloading media content."""

    media: Media | None
    content: DownloadContent | None
