import builtins
from collections.abc import Generator
from contextlib import contextmanager

from litestar.channels import ChannelsPlugin

from emitunes.bindings import models as bm
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

    def _emit_media_created_event(self, media: m.Media) -> None:
        """Emit a media created event."""

        data = ev.MediaCreatedEventData(
            media=media,
        )
        event = ev.MediaCreatedEvent(
            data=data,
        )
        self._emit_event(event)

    def _emit_media_updated_event(self, media: m.Media) -> None:
        """Emit a media updated event."""

        data = ev.MediaUpdatedEventData(
            media=media,
        )
        event = ev.MediaUpdatedEvent(
            data=data,
        )
        self._emit_event(event)

    def _emit_media_deleted_event(self, media: m.Media) -> None:
        """Emit a media deleted event."""

        data = ev.MediaDeletedEventData(
            media=media,
        )
        event = ev.MediaDeletedEvent(
            data=data,
        )
        self._emit_event(event)

    def _emit_binding_updated_event(self, binding: bm.Binding) -> None:
        """Emit a binding updated event."""

        data = ev.BindingUpdatedEventData(
            binding=binding,
        )
        event = ev.BindingUpdatedEvent(
            data=data,
        )
        self._emit_event(event)

    def _emit_binding_deleted_event(self, binding: bm.Binding) -> None:
        """Emit a binding deleted event."""

        data = ev.BindingDeletedEventData(
            binding=binding,
        )
        event = ev.BindingDeletedEvent(
            data=data,
        )
        self._emit_event(event)

    @contextmanager
    def _handle_errors(self) -> Generator[None, None, None]:
        try:
            yield
        except de.DataError as ex:
            raise e.ValidationError(str(ex)) from ex
        except de.DatatunesError as ex:
            raise e.DatatunesError(str(ex)) from ex
        except me.MediatunesError as ex:
            raise e.MediatunesError(str(ex)) from ex

    async def count(self, request: m.CountRequest) -> m.CountResponse:
        """Count media."""

        where = request.where

        with self._handle_errors():
            count = await self._datatunes.media.count(
                where=where,
            )

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

        with self._handle_errors():
            media = await self._datatunes.media.find_many(
                take=limit,
                skip=offset,
                where=where,
                include=include,
                order=order,
            )

        return m.ListResponse(
            media=media,
        )

    async def get(self, request: m.GetRequest) -> m.GetResponse:
        """Get media."""

        where = request.where
        include = request.include

        with self._handle_errors():
            media = await self._datatunes.media.find_unique(
                where=where,
                include=include,
            )

        return m.GetResponse(
            media=media,
        )

    async def create(self, request: m.CreateRequest) -> m.CreateResponse:
        """Create media."""

        data = request.data
        include = request.include

        with self._handle_errors():
            media = await self._datatunes.media.create(
                data=data,
                include=include,
            )

        self._emit_media_created_event(media)

        return m.CreateResponse(
            media=media,
        )

    async def _update_handle_bindings(
        self, transaction: DatatunesService, old: m.Media, new: m.Media
    ) -> builtins.list[bm.Binding]:
        bindings = []

        if new.id != old.id:
            bindings = await transaction.binding.find_many(
                where={"mediaId": old.id},
            )

            await transaction.binding.delete_many(
                where={"id": {"in": [binding.id for binding in bindings]}},
            )

            await transaction.media.create_many(
                data=[
                    {
                        "id": binding.id,
                        "playlistId": binding.playlistId,
                        "mediaId": new.id,
                        "rank": binding.rank,
                    }
                    for binding in bindings
                ],
            )

            bindings = await transaction.binding.find_many(
                where={"id": {"in": [binding.id for binding in bindings]}},
            )

        return bindings

    async def _update_handle_content(self, old: m.Media, new: m.Media) -> None:
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

    async def update(self, request: m.UpdateRequest) -> m.UpdateResponse:
        """Update media."""

        data = request.data
        where = request.where
        include = request.include

        async with self._datatunes.tx() as transaction:
            with self._handle_errors():
                old = await transaction.media.find_unique(
                    where=where,
                )

                if old is None:
                    return m.UpdateResponse(media=None)

                new = await transaction.media.update(
                    data=data,
                    where=where,
                    include=include,
                )

                if new is None:
                    return m.UpdateResponse(media=None)

                bindings = await self._update_handle_bindings(transaction, old, new)
                await self._update_handle_content(old, new)

        self._emit_media_updated_event(new)
        for binding in bindings:
            self._emit_binding_updated_event(binding)

        return m.UpdateResponse(
            media=new,
        )

    async def _delete_handle_bindings(
        self, transaction: DatatunesService, media: m.Media
    ) -> builtins.list[bm.Binding]:
        bindings = await transaction.binding.find_many(
            where={"mediaId": media.id},
        )

        await transaction.binding.delete_many(
            where={"id": {"in": [binding.id for binding in bindings]}},
        )

        return bindings

    async def _delete_handle_content(self, media: m.Media) -> None:
        try:
            await self._mediatunes.delete(
                mm.DeleteRequest(
                    name=media.id,
                )
            )
        except me.NotFoundError:
            pass

    async def delete(self, request: m.DeleteRequest) -> m.DeleteResponse:
        """Delete media."""

        where = request.where
        include = request.include

        async with self._datatunes.tx() as transaction:
            with self._handle_errors():
                media = await transaction.media.delete(
                    where=where,
                    include=include,
                )

                if media is None:
                    return m.DeleteResponse(
                        media=None,
                    )

                deleted = await self._delete_handle_bindings(transaction, media)
                await self._delete_handle_content(media)

        self._emit_media_deleted_event(media)
        for binding in deleted:
            self._emit_binding_deleted_event(binding)

        return m.DeleteResponse(
            media=media,
        )

    async def upload(self, request: m.UploadRequest) -> m.UploadResponse:
        """Upload media content."""

        where = request.where
        include = request.include
        content = request.content

        with self._handle_errors():
            media = await self._datatunes.media.find_unique(
                where=where,
                include=include,
            )

            if media is None:
                return m.UploadResponse(
                    media=None,
                )

            await self._mediatunes.upload(
                mm.UploadRequest(
                    name=media.id,
                    content=content,
                )
            )

        return m.UploadResponse(
            media=media,
        )

    async def download(self, request: m.DownloadRequest) -> m.DownloadResponse:
        """Download media content."""

        where = request.where
        include = request.include

        with self._handle_errors():
            media = await self._datatunes.media.find_unique(
                where=where,
                include=include,
            )

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

        return m.DownloadResponse(
            media=media,
            content=content,
        )
