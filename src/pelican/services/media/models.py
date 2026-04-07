from collections.abc import AsyncIterator, Sequence
from datetime import datetime

from pelican.models.base import datamodel
from pelican.services.graphite import models as gm
from pelican.services.graphite import types as gt
from pelican.utils.mime import MimeType

Binding = gm.Binding

Playlist = gm.Playlist

Media = gm.Media

MediaWhereInput = gt.MediaWhereInput

MediaInclude = gt.MediaInclude

MediaWhereUniqueIdInput = gt._MediaWhereUnique_id_Input  # noqa: SLF001

MediaWhereUniqueNameInput = gt._MediaWhereUnique_name_Input  # noqa: SLF001

type MediaWhereUniqueInput = MediaWhereUniqueIdInput | MediaWhereUniqueNameInput

MediaOrderByIdInput = gt._Media_id_OrderByInput  # noqa: SLF001

MediaOrderByNameInput = gt._Media_name_OrderByInput  # noqa: SLF001

type MediaOrderByInput = MediaOrderByIdInput | MediaOrderByNameInput

MediaCreateInput = gt.MediaCreateWithoutRelationsInput

MediaUpdateInput = gt.MediaUpdateManyMutationInput


@datamodel
class UploadContent:
    """Content model for upload."""

    type: MimeType
    """Content type."""

    data: AsyncIterator[bytes]
    """Asynchronous iterator of data bytes."""


@datamodel
class DownloadContent:
    """Content model for download."""

    type: MimeType
    """Content type."""

    size: int
    """Size of the content in bytes."""

    tag: str
    """ETag of the content."""

    modified: datetime
    """Date and time when the content was last modified."""

    data: AsyncIterator[bytes]
    """Asynchronous iterator of data bytes."""


@datamodel
class CountRequest:
    """Request to count media."""

    where: MediaWhereInput | None
    """Filter to apply to find media."""


@datamodel
class CountResponse:
    """Response for counting media."""

    count: int
    """Number of media that match the filter."""


@datamodel
class ListRequest:
    """Request to list media."""

    limit: int | None
    """Maximum number of media to return."""

    offset: int | None
    """Number of media to skip."""

    where: MediaWhereInput | None
    """Filter to apply to find media."""

    include: MediaInclude | None
    """Relations to include in the response."""

    order: MediaOrderByInput | Sequence[MediaOrderByInput] | None
    """Order to apply to the results."""


@datamodel
class ListResponse:
    """Response for listing media."""

    media: Sequence[Media]
    """List of media that match the filter."""


@datamodel
class GetRequest:
    """Request to get media."""

    where: MediaWhereUniqueInput
    """Unique filter to apply to find media."""

    include: MediaInclude | None
    """Relations to include in the response."""


@datamodel
class GetResponse:
    """Response for getting media."""

    media: Media | None
    """Media that matches the filter."""


@datamodel
class CreateRequest:
    """Request to create media."""

    data: MediaCreateInput
    """Data to create media."""

    include: MediaInclude | None
    """Relations to include in the response."""


@datamodel
class CreateResponse:
    """Response for creating media."""

    media: Media
    """Created media."""


@datamodel
class UpdateRequest:
    """Request to update media."""

    data: MediaUpdateInput
    """Data to update media."""

    where: MediaWhereUniqueInput
    """Unique filter to apply to find media."""

    include: MediaInclude | None
    """Relations to include in the response."""


@datamodel
class UpdateResponse:
    """Response for updating media."""

    media: Media | None
    """Updated media."""


@datamodel
class DeleteRequest:
    """Request to delete media."""

    where: MediaWhereUniqueInput
    """Unique filter to apply to find media."""

    include: MediaInclude | None
    """Relations to include in the response."""


@datamodel
class DeleteResponse:
    """Response for deleting media."""

    media: Media | None
    """Deleted media."""


@datamodel
class UploadRequest:
    """Request to upload media content."""

    where: MediaWhereUniqueInput
    """Unique filter to apply to find media."""

    include: MediaInclude | None
    """Relations to include in the response."""

    content: UploadContent
    """Content to upload."""


@datamodel
class UploadResponse:
    """Response for uploading media content."""

    media: Media | None
    """Media that was uploaded."""


@datamodel
class DownloadRequest:
    """Request to download media content."""

    where: MediaWhereUniqueInput
    """Unique filter to apply to find media."""

    include: MediaInclude | None
    """Relations to include in the response."""


@datamodel
class DownloadResponse:
    """Response for downloading media content."""

    media: Media | None
    """Media that was downloaded."""

    content: DownloadContent | None
    """Content that was downloaded."""
