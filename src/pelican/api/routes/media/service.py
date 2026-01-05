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
            raise e.ValidationError(str(ex)) from ex
        except me.GraphiteError as ex:
            raise e.GraphiteError(str(ex)) from ex
        except me.MiniumError as ex:
            raise e.MiniumError(str(ex)) from ex
        except me.ServiceError as ex:
            raise e.ServiceError(str(ex)) from ex

    async def list(self, request: m.ListRequest) -> m.ListResponse:
        """List media."""
        limit = request.limit
        offset = request.offset
        where = request.where
        include = request.include
        order = request.order

        req = mm.CountRequest(
            where=where,
        )

        with self._handle_errors():
            res = await self._media.count(req)

        count = res.count

        req = mm.ListRequest(
            limit=limit,
            offset=offset,
            where=where,
            include=include,
            order=order,
        )

        with self._handle_errors():
            res = await self._media.list(req)

        media = res.media

        media = [m.Media.map(med) for med in media]
        results = m.MediaList(
            count=count,
            limit=limit,
            offset=offset,
            media=media,
        )
        return m.ListResponse(
            results=results,
        )

    async def get(self, request: m.GetRequest) -> m.GetResponse:
        """Get media."""
        media_id = request.id
        include = request.include

        req = mm.GetRequest(
            where={
                "id": str(media_id),
            },
            include=include,
        )

        with self._handle_errors():
            res = await self._media.get(req)

        media = res.media

        if media is None:
            raise e.MediaNotFoundError(media_id)

        media = m.Media.map(media)
        return m.GetResponse(
            media=media,
        )

    async def create(self, request: m.CreateRequest) -> m.CreateResponse:
        """Create media."""
        data = request.data
        include = request.include

        req = mm.CreateRequest(
            data=data,
            include=include,
        )

        with self._handle_errors():
            res = await self._media.create(req)

        media = res.media

        media = m.Media.map(media)
        return m.CreateResponse(
            media=media,
        )

    async def update(self, request: m.UpdateRequest) -> m.UpdateResponse:
        """Update media."""
        data = request.data
        media_id = request.id
        include = request.include

        req = mm.UpdateRequest(
            data=data,
            where={
                "id": str(media_id),
            },
            include=include,
        )

        with self._handle_errors():
            res = await self._media.update(req)

        media = res.media

        if media is None:
            raise e.MediaNotFoundError(media_id)

        media = m.Media.map(media)
        return m.UpdateResponse(
            media=media,
        )

    async def delete(self, request: m.DeleteRequest) -> m.DeleteResponse:
        """Delete media."""
        media_id = request.id

        req = mm.DeleteRequest(
            where={
                "id": str(media_id),
            },
            include=None,
        )

        with self._handle_errors():
            res = await self._media.delete(req)

        media = res.media

        if media is None:
            raise e.MediaNotFoundError(media_id)

        return m.DeleteResponse()

    async def upload(self, request: m.UploadRequest) -> m.UploadResponse:
        """Upload media content."""
        media_id = request.id
        content_type = request.type
        data = request.data

        content = mm.UploadContent(
            type=content_type,
            data=data,
        )
        req = mm.UploadRequest(
            where={
                "id": str(media_id),
            },
            include=None,
            content=content,
        )

        with self._handle_errors():
            res = await self._media.upload(req)

        media = res.media

        if media is None:
            raise e.MediaNotFoundError(media_id)

        return m.UploadResponse()

    async def download(self, request: m.DownloadRequest) -> m.DownloadResponse:
        """Download media content."""
        media_id = request.id

        req = mm.DownloadRequest(
            where={
                "id": str(media_id),
            },
            include=None,
        )

        with self._handle_errors():
            res = await self._media.download(req)

        media = res.media

        if media is None:
            raise e.MediaNotFoundError(media_id)

        content = res.content

        if content is None:
            raise e.ContentNotFoundError(media_id)

        content_type = content.type
        size = content.size
        tag = content.tag
        modified = content.modified
        data = content.data

        return m.DownloadResponse(
            type=content_type,
            size=size,
            tag=tag,
            modified=modified,
            data=data,
        )

    async def headdownload(
        self, request: m.HeadDownloadRequest
    ) -> m.HeadDownloadResponse:
        """Download media content headers."""
        media_id = request.id

        req = mm.DownloadRequest(
            where={
                "id": str(media_id),
            },
            include=None,
        )

        with self._handle_errors():
            res = await self._media.download(req)

        media = res.media

        if media is None:
            raise e.MediaNotFoundError(media_id)

        content = res.content

        if content is None:
            raise e.ContentNotFoundError(media_id)

        content_type = content.type
        size = content.size
        tag = content.tag
        modified = content.modified

        return m.HeadDownloadResponse(
            type=content_type,
            size=size,
            tag=tag,
            modified=modified,
        )
