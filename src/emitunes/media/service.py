from litestar.channels import ChannelsPlugin

from emitunes.datatunes import errors as de
from emitunes.datatunes.service import DatatunesService
from emitunes.media import errors as e
from emitunes.media import models as m
from emitunes.mediatunes import errors as me
from emitunes.mediatunes import models as mm
from emitunes.mediatunes.service import MediatunesService
from emitunes.models import events as ev


class MediaService:
    """Service to manage media."""

    def __init__(
        self,
        datatunes: DatatunesService,
        mediatunes: MediatunesService,
        channels: ChannelsPlugin,
    ) -> None:
        self._datatunes = datatunes
        self._mediatunes = mediatunes
        self._channels = channels

    def _emit_event(self, event: ev.Event) -> None:
        """Emit an event."""

        data = event.model_dump_json(by_alias=True)
        self._channels.publish(data, "events")

    def _emit_created_event(self, media: m.Media) -> None:
        """Emit a media created event."""

        data = ev.MediaCreatedEventData(
            media=media,
        )
        event = ev.MediaCreatedEvent(
            data=data,
        )
        self._emit_event(event)

    def _emit_updated_event(self, media: m.Media) -> None:
        """Emit a media updated event."""

        data = ev.MediaUpdatedEventData(
            media=media,
        )
        event = ev.MediaUpdatedEvent(
            data=data,
        )
        self._emit_event(event)

    def _emit_deleted_event(self, media: m.Media) -> None:
        """Emit a media deleted event."""

        data = ev.MediaDeletedEventData(
            media=media,
        )
        event = ev.MediaDeletedEvent(
            data=data,
        )
        self._emit_event(event)

    async def count(self, request: m.CountRequest) -> m.CountResponse:
        """Count media."""

        where = request.where

        try:
            count = await self._datatunes.media.count(
                where=where,
            )
        except de.DataError as ex:
            raise e.ValidationError(str(ex)) from ex
        except de.DatatunesError as ex:
            raise e.DatatunesError(str(ex)) from ex

        return m.CountResponse(
            count=count,
        )

    async def list(self, request: m.ListRequest) -> m.ListResponse:
        """List all media."""

        limit = request.limit
        offset = request.offset
        where = request.where
        include = request.include
        order = request.order

        try:
            media = await self._datatunes.media.find_many(
                take=limit,
                skip=offset,
                where=where,
                include=include,
                order=order,
            )
        except de.DataError as ex:
            raise e.ValidationError(str(ex)) from ex
        except de.DatatunesError as ex:
            raise e.DatatunesError(str(ex)) from ex

        return m.ListResponse(
            media=media,
        )

    async def get(self, request: m.GetRequest) -> m.GetResponse:
        """Get media."""

        where = request.where
        include = request.include

        try:
            media = await self._datatunes.media.find_unique(
                where=where,
                include=include,
            )
        except de.DataError as ex:
            raise e.ValidationError(str(ex)) from ex
        except de.DatatunesError as ex:
            raise e.DatatunesError(str(ex)) from ex

        return m.GetResponse(
            media=media,
        )

    async def create(self, request: m.CreateRequest) -> m.CreateResponse:
        """Create media."""

        data = request.data
        include = request.include

        try:
            media = await self._datatunes.media.create(
                data=data,
                include=include,
            )
        except de.DataError as ex:
            raise e.ValidationError(str(ex)) from ex
        except de.DatatunesError as ex:
            raise e.DatatunesError(str(ex)) from ex

        self._emit_created_event(media)

        return m.CreateResponse(
            media=media,
        )

    async def update(self, request: m.UpdateRequest) -> m.UpdateResponse:
        """Update media."""

        data = request.data
        where = request.where
        include = request.include

        async with self._datatunes.tx() as transaction:
            try:
                old = await transaction.media.find_unique(
                    where=where,
                )
            except de.DataError as ex:
                raise e.ValidationError(str(ex)) from ex
            except de.DatatunesError as ex:
                raise e.DatatunesError(str(ex)) from ex

            if old is None:
                return m.UpdateResponse(media=None)

            try:
                new = await transaction.media.update(
                    data=data,
                    where=where,
                    include=include,
                )
            except de.DataError as ex:
                raise e.ValidationError(str(ex)) from ex
            except de.DatatunesError as ex:
                raise e.DatatunesError(str(ex)) from ex

            if new is None:
                return m.UpdateResponse(media=None)

            if new.id != old.id:
                try:
                    await self._mediatunes.copy(
                        mm.CopyRequest(
                            source=old.id,
                            destination=new.id,
                        )
                    )
                    await self._mediatunes.delete(
                        mm.DeleteRequest(
                            name=old.id,
                        )
                    )
                except me.NotFoundError:
                    pass
                except me.MediatunesError as ex:
                    raise e.MediatunesError(str(ex)) from ex

        self._emit_updated_event(new)

        return m.UpdateResponse(
            media=new,
        )

    async def delete(self, request: m.DeleteRequest) -> m.DeleteResponse:
        """Delete media."""

        where = request.where
        include = request.include

        async with self._datatunes.tx() as transaction:
            try:
                media = await transaction.media.delete(
                    where=where,
                    include=include,
                )
            except de.DataError as ex:
                raise e.ValidationError(str(ex)) from ex
            except de.DatatunesError as ex:
                raise e.DatatunesError(str(ex)) from ex

            if media is None:
                return m.DeleteResponse(
                    media=None,
                )

            try:
                await self._mediatunes.delete(
                    mm.DeleteRequest(
                        name=media.id,
                    )
                )
            except me.NotFoundError:
                pass
            except me.MediatunesError as ex:
                raise e.MediatunesError(str(ex)) from ex

        self._emit_deleted_event(media)

        return m.DeleteResponse(
            media=media,
        )

    async def upload(self, request: m.UploadRequest) -> m.UploadResponse:
        """Upload media content."""

        where = request.where
        include = request.include
        content = request.content

        try:
            media = await self._datatunes.media.find_unique(
                where=where,
                include=include,
            )
        except de.DataError as ex:
            raise e.ValidationError(str(ex)) from ex
        except de.DatatunesError as ex:
            raise e.DatatunesError(str(ex)) from ex

        if media is None:
            return m.UploadResponse(
                media=None,
            )

        try:
            await self._mediatunes.upload(
                mm.UploadRequest(
                    name=media.id,
                    content=content,
                )
            )
        except me.MediatunesError as ex:
            raise e.MediatunesError(str(ex)) from ex

        return m.UploadResponse(
            media=media,
        )

    async def download(self, request: m.DownloadRequest) -> m.DownloadResponse:
        """Download media content."""

        where = request.where
        include = request.include

        try:
            media = await self._datatunes.media.find_unique(
                where=where,
                include=include,
            )
        except de.DataError as ex:
            raise e.ValidationError(str(ex)) from ex
        except de.DatatunesError as ex:
            raise e.DatatunesError(str(ex)) from ex

        if media is None:
            return m.DownloadResponse(
                media=None,
                content=None,
            )

        try:
            response = await self._mediatunes.download(
                mm.DownloadRequest(
                    name=media.id,
                )
            )
            content = response.content
        except me.NotFoundError:
            return m.DownloadResponse(
                media=media,
                content=None,
            )
        except me.MediatunesError as ex:
            raise e.MediatunesError(str(ex)) from ex

        return m.DownloadResponse(
            media=media,
            content=content,
        )
