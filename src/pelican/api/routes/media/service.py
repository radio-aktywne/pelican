from collections.abc import Generator
from contextlib import contextmanager

from pelican.api.routes.media import errors as e
from pelican.api.routes.media import models as m
from pelican.services.media import errors as me
from pelican.services.media import models as mm
from pelican.services.media.service import MediaService


class Service:
    """Service for the media endpoint."""

    def __init__(self, media: MediaService) -> None:
        self._media = media

    @contextmanager
    def _handle_errors(self) -> Generator[None]:
        try:
            yield
        except me.ValidationError as ex:
            raise e.ValidationError from ex
        except me.GraphiteError as ex:
            raise e.GraphiteError from ex
        except me.MiniumError as ex:
            raise e.MiniumError from ex
        except me.ServiceError as ex:
            raise e.ServiceError from ex

    async def list(self, request: m.ListRequest) -> m.ListResponse:
        """List media."""
        count_request = mm.CountRequest(where=request.where)

        with self._handle_errors():
            count_response = await self._media.count(count_request)

        list_request = mm.ListRequest(
            limit=request.limit,
            offset=request.offset,
            where=request.where,
            include=request.include,
            order=request.order,
        )

        with self._handle_errors():
            list_response = await self._media.list(list_request)

        return m.ListResponse(
            results=m.MediaList(
                count=count_response.count,
                limit=request.limit,
                offset=request.offset,
                media=[m.Media.map(med) for med in list_response.media],
            )
        )

    async def get(self, request: m.GetRequest) -> m.GetResponse:
        """Get media."""
        get_request = mm.GetRequest(
            where={"id": str(request.id)}, include=request.include
        )

        with self._handle_errors():
            get_response = await self._media.get(get_request)

        if get_response.media is None:
            raise e.MediaNotFoundError(request.id)

        return m.GetResponse(media=m.Media.map(get_response.media))

    async def create(self, request: m.CreateRequest) -> m.CreateResponse:
        """Create media."""
        create_request = mm.CreateRequest(data=request.data, include=request.include)

        with self._handle_errors():
            create_response = await self._media.create(create_request)

        return m.CreateResponse(media=m.Media.map(create_response.media))

    async def update(self, request: m.UpdateRequest) -> m.UpdateResponse:
        """Update media."""
        update_request = mm.UpdateRequest(
            data=request.data, where={"id": str(request.id)}, include=request.include
        )

        with self._handle_errors():
            update_response = await self._media.update(update_request)

        if update_response.media is None:
            raise e.MediaNotFoundError(request.id)

        return m.UpdateResponse(media=m.Media.map(update_response.media))

    async def delete(self, request: m.DeleteRequest) -> m.DeleteResponse:
        """Delete media."""
        delete_request = mm.DeleteRequest(where={"id": str(request.id)}, include=None)

        with self._handle_errors():
            delete_response = await self._media.delete(delete_request)

        if delete_response.media is None:
            raise e.MediaNotFoundError(request.id)

        return m.DeleteResponse()

    async def upload(self, request: m.UploadRequest) -> m.UploadResponse:
        """Upload media content."""
        upload_request = mm.UploadRequest(
            where={"id": str(request.id)},
            include=None,
            content=mm.UploadContent(type=request.type, data=request.data),
        )

        with self._handle_errors():
            upload_response = await self._media.upload(upload_request)

        if upload_response.media is None:
            raise e.MediaNotFoundError(request.id)

        return m.UploadResponse()

    async def download(self, request: m.DownloadRequest) -> m.DownloadResponse:
        """Download media content."""
        download_request = mm.DownloadRequest(
            where={"id": str(request.id)}, include=None
        )

        with self._handle_errors():
            download_response = await self._media.download(download_request)

        if download_response.media is None:
            raise e.MediaNotFoundError(request.id)

        if download_response.content is None:
            raise e.ContentNotFoundError(request.id)

        return m.DownloadResponse(
            type=download_response.content.type,
            size=download_response.content.size,
            tag=download_response.content.tag,
            modified=download_response.content.modified,
            data=download_response.content.data,
        )

    async def headdownload(
        self, request: m.HeadDownloadRequest
    ) -> m.HeadDownloadResponse:
        """Download media content headers."""
        download_request = mm.DownloadRequest(
            where={"id": str(request.id)}, include=None
        )

        with self._handle_errors():
            download_response = await self._media.download(download_request)

        if download_response.media is None:
            raise e.MediaNotFoundError(request.id)

        if download_response.content is None:
            raise e.ContentNotFoundError(request.id)

        return m.HeadDownloadResponse(
            type=download_response.content.type,
            size=download_response.content.size,
            tag=download_response.content.tag,
            modified=download_response.content.modified,
        )
