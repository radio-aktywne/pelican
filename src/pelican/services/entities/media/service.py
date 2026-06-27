from collections.abc import Generator, Sequence
from contextlib import contextmanager
from typing import cast

from pelican.services.data.graphite import errors as ge
from pelican.services.data.graphite import types as gt
from pelican.services.data.graphite.service import GraphiteService
from pelican.services.data.minium import errors as me
from pelican.services.data.minium import models as mm
from pelican.services.data.minium.service import MiniumService
from pelican.services.entities.media import errors as e
from pelican.services.entities.media import models as m
from pelican.services.entities.media.utils import ContentTypeChecker
from pelican.utils.mime import MimeType, MimeTypeValidationError


class MediaService:
    """Service to manage media."""

    def __init__(self, graphite: GraphiteService, minium: MiniumService) -> None:
        self._graphite = graphite
        self._minium = minium

    @contextmanager
    def _handle_errors(self) -> Generator[None]:
        try:
            yield
        except ge.UniqueViolationError as ex:
            raise e.ConflictError from ex
        except ge.DataError as ex:
            raise e.ValidationError from ex
        except (ge.ServiceError, me.ServiceError) as ex:
            raise e.ServiceError from ex

    async def count(self, request: m.CountRequest) -> m.CountResponse:
        """Count media."""
        with self._handle_errors():
            count = await self._graphite.media.count(where=request.where)

        return m.CountResponse(count=count)

    async def list(self, request: m.ListRequest) -> m.ListResponse:
        """List all media."""
        with self._handle_errors():
            media = await self._graphite.media.find_many(
                take=request.limit,
                skip=request.offset,
                where=request.where,
                include=request.include,
                order=list(request.order)
                if isinstance(request.order, Sequence)
                else request.order,
            )

        return m.ListResponse(media=media)

    async def get(self, request: m.GetRequest) -> m.GetResponse:
        """Get media."""
        with self._handle_errors():
            media = await self._graphite.media.find_unique(
                where=request.where, include=request.include
            )

        return m.GetResponse(media=media)

    async def create(self, request: m.CreateRequest) -> m.CreateResponse:
        """Create media."""
        with self._handle_errors():
            media = await self._graphite.media.create(
                data=cast("gt.MediaCreateInput", request.data), include=request.include
            )

        return m.CreateResponse(media=media)

    async def _update_handle_content(self, old: m.Media, new: m.Media) -> None:
        if new.id != old.id:
            try:
                copy_request = mm.CopyRequest(source=old.id, destination=new.id)
                await self._minium.copy(copy_request)

                delete_request = mm.DeleteRequest(name=old.id)
                await self._minium.delete(delete_request)
            except me.NotFoundError:
                pass

    async def update(self, request: m.UpdateRequest) -> m.UpdateResponse:
        """Update media."""
        async with self._graphite.tx() as transaction:
            with self._handle_errors():
                old = await transaction.media.find_unique(where=request.where)

                if old is None:
                    return m.UpdateResponse(media=None)

                new = await transaction.media.update(
                    data=cast("gt.MediaUpdateInput", request.data),
                    where=request.where,
                    include=request.include,
                )

                if new is None:
                    return m.UpdateResponse(media=None)

                await self._update_handle_content(old, new)

        return m.UpdateResponse(media=new)

    async def _delete_handle_content(self, media: m.Media) -> None:
        try:
            delete_request = mm.DeleteRequest(name=media.id)
            await self._minium.delete(delete_request)
        except me.NotFoundError:
            pass

    async def delete(self, request: m.DeleteRequest) -> m.DeleteResponse:
        """Delete media."""
        async with self._graphite.tx() as transaction:
            with self._handle_errors():
                media = await transaction.media.delete(
                    where=request.where, include=request.include
                )

                if media is None:
                    return m.DeleteResponse(media=None)

                await self._delete_handle_content(media)

        return m.DeleteResponse(media=media)

    async def upload(self, request: m.UploadRequest) -> m.UploadResponse:
        """Upload media content."""
        if not ContentTypeChecker().check(request.content.type):
            raise e.UnsupportedContentTypeError(request.content.type)

        with self._handle_errors():
            media = await self._graphite.media.find_unique(
                where=request.where, include=request.include
            )

            if media is None:
                return m.UploadResponse(media=None)

            upload_request = mm.UploadRequest(
                name=media.id,
                content=mm.UploadContent(
                    type=str(request.content.type), data=request.content.data
                ),
            )
            await self._minium.upload(upload_request)

        return m.UploadResponse(media=media)

    async def download(self, request: m.DownloadRequest) -> m.DownloadResponse:
        """Download media content."""
        with self._handle_errors():
            media = await self._graphite.media.find_unique(
                where=request.where, include=request.include
            )

            if media is None:
                return m.DownloadResponse(media=None, content=None)

            try:
                download_request = mm.DownloadRequest(name=media.id)
                download_response = await self._minium.download(download_request)
            except me.NotFoundError:
                return m.DownloadResponse(media=media, content=None)

        try:
            try:
                content = m.DownloadContent(
                    type=MimeType.parse(download_response.content.type),
                    size=download_response.content.size,
                    tag=download_response.content.tag,
                    modified=download_response.content.modified,
                    data=download_response.content.data,
                )
            except MimeTypeValidationError:
                await download_response.content.data.aclose()
                return m.DownloadResponse(media=media, content=None)

            if not ContentTypeChecker().check(content.type):
                await download_response.content.data.aclose()
                return m.DownloadResponse(media=media, content=None)

            return m.DownloadResponse(media=media, content=content)
        except:
            await download_response.content.data.aclose()
            raise
