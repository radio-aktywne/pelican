import builtins
from collections.abc import Generator
from contextlib import contextmanager

from litestar.channels import ChannelsPlugin

from emitunes.models.events import binding as bev
from emitunes.models.events import media as mev
from emitunes.models.events.event import Event
from emitunes.services.bindings import models as bm
from emitunes.services.datatunes import errors as de
from emitunes.services.datatunes.service import DatatunesService
from emitunes.services.media import errors as e
from emitunes.services.media import models as m
from emitunes.services.mediatunes import errors as me
from emitunes.services.mediatunes import models as mm
from emitunes.services.mediatunes.service import MediatunesService


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

    def _emit_event(self, event: Event) -> None:
        data = event.model_dump_json(by_alias=True)
        self._channels.publish(data, "events")

    def _emit_media_created_event(self, media: m.Media) -> None:
        media = mev.Media.map(media)
        data = mev.MediaCreatedEventData(
            media=media,
        )
        event = mev.MediaCreatedEvent(
            data=data,
        )
        self._emit_event(event)

    def _emit_media_updated_event(self, media: m.Media) -> None:
        media = mev.Media.map(media)
        data = mev.MediaUpdatedEventData(
            media=media,
        )
        event = mev.MediaUpdatedEvent(
            data=data,
        )
        self._emit_event(event)

    def _emit_media_deleted_event(self, media: m.Media) -> None:
        media = mev.Media.map(media)
        data = mev.MediaDeletedEventData(
            media=media,
        )
        event = mev.MediaDeletedEvent(
            data=data,
        )
        self._emit_event(event)

    def _emit_binding_updated_event(self, binding: bm.Binding) -> None:
        binding = bev.Binding.map(binding)
        data = bev.BindingUpdatedEventData(
            binding=binding,
        )
        event = bev.BindingUpdatedEvent(
            data=data,
        )
        self._emit_event(event)

    def _emit_binding_deleted_event(self, binding: bm.Binding) -> None:
        binding = bev.Binding.map(binding)
        data = bev.BindingDeletedEventData(
            binding=binding,
        )
        event = bev.BindingDeletedEvent(
            data=data,
        )
        self._emit_event(event)

    @contextmanager
    def _handle_errors(self) -> Generator[None]:
        try:
            yield
        except de.DataError as ex:
            raise e.ValidationError(str(ex)) from ex
        except de.ServiceError as ex:
            raise e.DatatunesError(str(ex)) from ex
        except me.ServiceError as ex:
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
                where={
                    "mediaId": old.id,
                },
            )

            ids = [binding.id for binding in bindings]

            await transaction.binding.delete_many(
                where={
                    "id": {
                        "in": ids,
                    },
                },
            )

            await transaction.binding.create_many(
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
                where={
                    "id": {
                        "in": ids,
                    },
                },
            )

        return bindings

    async def _update_handle_content(self, old: m.Media, new: m.Media) -> None:
        if new.id != old.id:
            try:
                req = mm.CopyRequest(
                    source=old.id,
                    destination=new.id,
                )

                await self._mediatunes.copy(req)

                req = mm.DeleteRequest(
                    name=old.id,
                )

                await self._mediatunes.delete(req)
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
                    return m.UpdateResponse(
                        media=None,
                    )

                new = await transaction.media.update(
                    data=data,
                    where=where,
                    include=include,
                )

                if new is None:
                    return m.UpdateResponse(
                        media=None,
                    )

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
            where={
                "mediaId": media.id,
            },
        )

        await transaction.binding.delete_many(
            where={
                "id": {
                    "in": [binding.id for binding in bindings],
                },
            },
        )

        return bindings

    async def _delete_handle_content(self, media: m.Media) -> None:
        try:
            req = mm.DeleteRequest(
                name=media.id,
            )

            await self._mediatunes.delete(req)
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

            req = mm.UploadRequest(
                name=media.id,
                content=content,
            )

            await self._mediatunes.upload(req)

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
                req = mm.DownloadRequest(
                    name=media.id,
                )

                res = await self._mediatunes.download(req)

                content = res.content
            except me.NotFoundError:
                return m.DownloadResponse(
                    media=media,
                    content=None,
                )

        return m.DownloadResponse(
            media=media,
            content=content,
        )
