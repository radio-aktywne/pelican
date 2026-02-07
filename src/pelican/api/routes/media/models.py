from collections.abc import AsyncIterator, Sequence
from datetime import datetime
from typing import Self
from uuid import UUID

from pelican.models.base import SerializableModel, datamodel
from pelican.services.media import models as mm


class Binding(SerializableModel):
    """Binding data."""

    id: UUID
    """Identifier of the binding."""

    playlist_id: UUID
    """Identifier of the playlist that the binding belongs to."""

    media_id: UUID
    """Identifier of the media that the binding belongs to."""

    rank: str
    """Rank of the media in the binding."""

    playlist: "Playlist | None"
    """Playlist that the binding belongs to."""

    media: "Media | None"
    """Media that the binding belongs to."""

    @classmethod
    def map(cls, binding: mm.Binding) -> Self:
        """Map to internal representation."""
        return cls(
            id=UUID(binding.id),
            playlist_id=UUID(binding.playlistId),
            media_id=UUID(binding.mediaId),
            rank=binding.rank,
            playlist=Playlist.map(binding.playlist) if binding.playlist else None,
            media=Media.map(binding.media) if binding.media else None,
        )


class Playlist(SerializableModel):
    """Playlist data."""

    id: UUID
    """Identifier of the playlist."""

    name: str
    """Name of the playlist."""

    bindings: Sequence[Binding] | None
    """Bindings that the playlist belongs to."""

    @classmethod
    def map(cls, playlist: mm.Playlist) -> Self:
        """Map to internal representation."""
        return cls(
            id=UUID(playlist.id),
            name=playlist.name,
            bindings=(
                [Binding.map(binding) for binding in playlist.bindings]
                if playlist.bindings is not None
                else None
            ),
        )


class Media(SerializableModel):
    """Media data."""

    id: UUID
    """Identifier of the media."""

    name: str
    """Name of the media."""

    bindings: Sequence[Binding] | None
    """Bindings that the media belongs to."""

    @classmethod
    def map(cls, media: mm.Media) -> Self:
        """Map to internal representation."""
        return cls(
            id=UUID(media.id),
            name=media.name,
            bindings=(
                [Binding.map(binding) for binding in media.bindings]
                if media.bindings is not None
                else None
            ),
        )


class MediaList(SerializableModel):
    """List of media."""

    count: int
    """Total number of media that matched the query."""

    limit: int | None
    """Maximum number of returned media."""

    offset: int | None
    """Number of media skipped."""

    media: Sequence[Media]
    """Media that matched the request."""


MediaWhereInput = mm.MediaWhereInput

MediaWhereUniqueIdInput = mm.MediaWhereUniqueIdInput

MediaWhereUniqueNameInput = mm.MediaWhereUniqueNameInput

type MediaWhereUniqueInput = MediaWhereUniqueIdInput | MediaWhereUniqueNameInput

MediaInclude = mm.MediaInclude

MediaOrderByIdInput = mm.MediaOrderByIdInput

MediaOrderByNameInput = mm.MediaOrderByNameInput

type MediaOrderByInput = MediaOrderByIdInput | MediaOrderByNameInput

MediaCreateInput = mm.MediaCreateInput

MediaUpdateInput = mm.MediaUpdateInput

type ListRequestLimit = int | None

type ListRequestOffset = int | None

type ListRequestWhere = MediaWhereInput | None

type ListRequestInclude = MediaInclude | None

type ListRequestOrder = MediaOrderByInput | Sequence[MediaOrderByInput] | None

type ListResponseResults = MediaList

type GetRequestId = UUID

type GetRequestInclude = MediaInclude | None

type GetResponseMedia = Media

type CreateRequestData = MediaCreateInput

type CreateRequestInclude = MediaInclude | None

type CreateResponseMedia = Media

type UpdateRequestData = MediaUpdateInput

type UpdateRequestId = UUID

type UpdateRequestInclude = MediaInclude | None

type UpdateResponseMedia = Media

type DeleteRequestId = UUID

type UploadRequestId = UUID

type UploadRequestType = str

type UploadRequestData = AsyncIterator[bytes]

type DownloadRequestId = UUID

type DownloadResponseType = str

type DownloadResponseSize = int

type DownloadResponseTag = str

type DownloadResponseModified = datetime

type DownloadResponseData = AsyncIterator[bytes]

type HeadDownloadRequestId = UUID

type HeadDownloadResponseType = str

type HeadDownloadResponseSize = int

type HeadDownloadResponseTag = str

type HeadDownloadResponseModified = datetime


@datamodel
class ListRequest:
    """Request to list media."""

    limit: ListRequestLimit
    """Maximum number of media to return."""

    offset: ListRequestOffset
    """Number of media to skip."""

    where: ListRequestWhere
    """Filter to apply to find media."""

    include: ListRequestInclude
    """Relations to include in the response."""

    order: ListRequestOrder
    """Order to apply to the results."""


@datamodel
class ListResponse:
    """Response for listing media."""

    results: ListResponseResults
    """List of media."""


@datamodel
class GetRequest:
    """Request to get media."""

    id: GetRequestId
    """Identifier of the media to get."""

    include: GetRequestInclude
    """Relations to include in the response."""


@datamodel
class GetResponse:
    """Response for getting media."""

    media: GetResponseMedia
    """Media that matched the request."""


@datamodel
class CreateRequest:
    """Request to create media."""

    data: CreateRequestData
    """Data to create media."""

    include: CreateRequestInclude
    """Relations to include in the response."""


@datamodel
class CreateResponse:
    """Response for creating media."""

    media: CreateResponseMedia
    """Media that was created."""


@datamodel
class UpdateRequest:
    """Request to update media."""

    data: UpdateRequestData
    """Data to update media."""

    id: UpdateRequestId
    """Identifier of the media to update."""

    include: UpdateRequestInclude
    """Relations to include in the response."""


@datamodel
class UpdateResponse:
    """Response for updating media."""

    media: UpdateResponseMedia
    """Media that was updated."""


@datamodel
class DeleteRequest:
    """Request to delete media."""

    id: DeleteRequestId
    """Identifier of the media to delete."""


@datamodel
class DeleteResponse:
    """Response for deleting media."""


@datamodel
class UploadRequest:
    """Request to upload media content."""

    id: UploadRequestId
    """Identifier of the media to upload content for."""

    type: UploadRequestType
    """Type of the content."""

    data: UploadRequestData
    """Data of the content."""


@datamodel
class UploadResponse:
    """Response for uploading media content."""


@datamodel
class DownloadRequest:
    """Request to download media content."""

    id: DownloadRequestId
    """Identifier of the media to download content for."""


@datamodel
class DownloadResponse:
    """Response for downloading media content."""

    type: DownloadResponseType
    """Type of the content."""

    size: DownloadResponseSize
    """Size of the content in bytes."""

    tag: DownloadResponseTag
    """ETag of the content."""

    modified: DownloadResponseModified
    """Date and time when the content was last modified."""

    data: DownloadResponseData
    """Data of the content."""


@datamodel
class HeadDownloadRequest:
    """Request to download media content headers."""

    id: HeadDownloadRequestId
    """Identifier of the media to download content headers for."""


@datamodel
class HeadDownloadResponse:
    """Response for downloading media content headers."""

    type: HeadDownloadResponseType
    """Type of the content."""

    size: HeadDownloadResponseSize
    """Size of the content in bytes."""

    tag: HeadDownloadResponseTag
    """ETag of the content."""

    modified: HeadDownloadResponseModified
    """Date and time when the content was last modified."""
