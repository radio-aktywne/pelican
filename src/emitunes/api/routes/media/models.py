from uuid import UUID

from emitunes.models.base import SerializableModel, datamodel, serializable
from emitunes.services.bindings import models as bm
from emitunes.services.media import models as mm
from emitunes.services.playlists import models as pm


class Binding(SerializableModel):
    """Binding data."""

    id: str
    """Identifier of the binding."""

    playlist_id: str
    """Identifier of the playlist that the binding belongs to."""

    media_id: str
    """Identifier of the media that the binding belongs to."""

    rank: str
    """Rank of the media in the binding."""

    playlist: "Playlist | None"
    """Playlist that the binding belongs to."""

    media: "Media | None"
    """Media that the binding belongs to."""

    @staticmethod
    def map(binding: bm.Binding) -> "Binding":
        return Binding(
            id=binding.id,
            playlist_id=binding.playlistId,
            media_id=binding.mediaId,
            rank=binding.rank,
            playlist=Playlist.map(binding.playlist) if binding.playlist else None,
            media=Media.map(binding.media) if binding.media else None,
        )


class Playlist(SerializableModel):
    """Playlist data."""

    id: str
    """Identifier of the playlist."""

    name: str
    """Name of the playlist."""

    bindings: list[Binding] | None
    """Bindings that the playlist belongs to."""

    @staticmethod
    def map(playlist: pm.Playlist) -> "Playlist":
        return Playlist(
            id=playlist.id,
            name=playlist.name,
            bindings=(
                [Binding.map(binding) for binding in playlist.bindings]
                if playlist.bindings is not None
                else None
            ),
        )


class Media(SerializableModel):
    """Media data."""

    id: str
    """Identifier of the media."""

    name: str
    """Name of the media."""

    bindings: list[Binding] | None
    """Bindings that the media belongs to."""

    @staticmethod
    def map(media: mm.Media) -> "Media":
        return Media(
            id=media.id,
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

    media: list[Media]
    """Media that matched the request."""


@serializable
class MediaWhereInput(mm.MediaWhereInput):
    pass


@serializable
class MediaWhereUniqueIdInput(mm.MediaWhereUniqueIdInput):
    pass


@serializable
class MediaWhereUniqueNameInput(mm.MediaWhereUniqueNameInput):
    pass


MediaWhereUniqueInput = MediaWhereUniqueIdInput | MediaWhereUniqueNameInput


@serializable
class MediaInclude(mm.MediaInclude):
    pass


@serializable
class MediaOrderByIdInput(mm.MediaOrderByIdInput):
    pass


@serializable
class MediaOrderByNameInput(mm.MediaOrderByNameInput):
    pass


MediaOrderByInput = MediaOrderByIdInput | MediaOrderByNameInput


@serializable
class MediaCreateInput(mm.MediaCreateInput):
    pass


@serializable
class MediaUpdateInput(mm.MediaUpdateInput):
    pass


@serializable
class UploadContent(mm.UploadContent):
    def map(self) -> mm.UploadContent:
        return mm.UploadContent(**vars(self))


@serializable
class DownloadContent(mm.DownloadContent):
    @staticmethod
    def map(content: mm.DownloadContent) -> "DownloadContent":
        return DownloadContent(**vars(content))


ListRequestLimit = int | None

ListRequestOffset = int | None

ListRequestWhere = MediaWhereInput | None

ListRequestInclude = MediaInclude | None

ListRequestOrder = MediaOrderByInput | list[MediaOrderByInput] | None

ListResponseResults = MediaList

GetRequestId = UUID

GetRequestInclude = MediaInclude | None

GetResponseMedia = Media

CreateRequestData = MediaCreateInput

CreateRequestInclude = MediaInclude | None

CreateResponseMedia = Media

UpdateRequestData = MediaUpdateInput

UpdateRequestId = UUID

UpdateRequestInclude = MediaInclude | None

UpdateResponseMedia = Media

DeleteRequestId = UUID

UploadRequestId = UUID

UploadRequestContent = UploadContent

DownloadRequestId = UUID

DownloadResponseContent = DownloadContent

HeadDownloadRequestId = UUID

HeadDownloadResponseContent = DownloadContent


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

    pass


@datamodel
class UploadRequest:
    """Request to upload media content."""

    id: UploadRequestId
    """Identifier of the media to upload content for."""

    content: UploadRequestContent
    """Content to upload."""


@datamodel
class UploadResponse:
    """Response for uploading media content."""

    pass


@datamodel
class DownloadRequest:
    """Request to download media content."""

    id: DownloadRequestId
    """Identifier of the media to download content for."""


@datamodel
class DownloadResponse:
    """Response for downloading media content."""

    content: DownloadResponseContent
    """Content that was downloaded."""


@datamodel
class HeadDownloadRequest:
    """Request to download media content headers."""

    id: HeadDownloadRequestId
    """Identifier of the media to download content headers for."""


@datamodel
class HeadDownloadResponse:
    """Response for downloading media content headers."""

    content: HeadDownloadResponseContent
    """Content that was downloaded."""
