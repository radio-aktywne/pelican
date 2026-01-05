from collections.abc import Generator, Sequence
from contextlib import contextmanager
from typing import cast

from litestar.channels import ChannelsPlugin

from pelican.models.events import binding as bev
from pelican.models.events import media as mev
from pelican.models.events.event import Event
from pelican.services.graphite import errors as ge
from pelican.services.graphite import types as gt
from pelican.services.graphite.service import GraphiteService
from pelican.services.media import errors as e
from pelican.services.media import models as m
from pelican.services.minium import errors as me
from pelican.services.minium import models as mm
from pelican.services.minium.service import MiniumService


class MediaService:
    """Service to manage media."""

    def __init__(
        self,
        graphite: GraphiteService,
        minium: MiniumService,
        channels: ChannelsPlugin,
    ) -> None:
        self._graphite = graphite
        self._minium = minium
        self._channels = channels

    def _emit_event(self, event: Event) -> None:
        data = event.model_dump_json(by_alias=True)
        self._channels.publish(data, "events")

    def _emit_media_created_event(self, media: m.Media) -> None:
        mapped_media = mev.Media.map(media)
        created_event_data = mev.MediaCreatedEventData(
            media=mapped_media,
        )
        created_event = mev.MediaCreatedEvent(
            data=created_event_data,
        )
        self._emit_event(created_event)

    def _emit_media_updated_event(self, media: m.Media) -> None:
        mapped_media = mev.Media.map(media)
        updated_event_data = mev.MediaUpdatedEventData(
            media=mapped_media,
        )
        updated_event = mev.MediaUpdatedEvent(
            data=updated_event_data,
        )
        self._emit_event(updated_event)

    def _emit_media_deleted_event(self, media: m.Media) -> None:
        mapped_media = mev.Media.map(media)
        deleted_event_data = mev.MediaDeletedEventData(
            media=mapped_media,
        )
        deleted_event = mev.MediaDeletedEvent(
            data=deleted_event_data,
        )
        self._emit_event(deleted_event)

    def _emit_binding_updated_event(self, binding: m.Binding) -> None:
        mapped_binding = bev.Binding.map(binding)
        updated_event_data = bev.BindingUpdatedEventData(
            binding=mapped_binding,
        )
        updated_event = bev.BindingUpdatedEvent(
            data=updated_event_data,
        )
        self._emit_event(updated_event)

    def _emit_binding_deleted_event(self, binding: m.Binding) -> None:
        mapped_binding = bev.Binding.map(binding)
        deleted_event_data = bev.BindingDeletedEventData(
            binding=mapped_binding,
        )
        deleted_event = bev.BindingDeletedEvent(
            data=deleted_event_data,
        )
        self._emit_event(deleted_event)

    @contextmanager
    def _handle_errors(self) -> Generator[None]:
        try:
            yield
        except ge.DataError as ex:
            raise e.ValidationError(str(ex)) from ex
        except ge.ServiceError as ex:
            raise e.GraphiteError(str(ex)) from ex
        except me.ServiceError as ex:
            raise e.MiniumError(str(ex)) from ex

    async def count(self, request: m.CountRequest) -> m.CountResponse:
        """Count media."""
        where = request.where

        with self._handle_errors():
            count = await self._graphite.media.count(
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
            media = await self._graphite.media.find_many(
                take=limit,
                skip=offset,
                where=where,
                include=include,
                order=list(order) if isinstance(order, Sequence) else order,
            )

        return m.ListResponse(
            media=media,
        )

    async def get(self, request: m.GetRequest) -> m.GetResponse:
        """Get media."""
        where = request.where
        include = request.include

        with self._handle_errors():
            media = await self._graphite.media.find_unique(
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
            media = await self._graphite.media.create(
                data=cast("gt.MediaCreateInput", data),
                include=include,
            )

        self._emit_media_created_event(media)

        return m.CreateResponse(
            media=media,
        )

    async def _update_handle_bindings(
        self, transaction: GraphiteService, old: m.Media, new: m.Media
    ) -> Sequence[m.Binding]:
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

                await self._minium.copy(req)

                req = mm.DeleteRequest(
                    name=old.id,
                )

                await self._minium.delete(req)
            except me.NotFoundError:
                pass

    async def update(self, request: m.UpdateRequest) -> m.UpdateResponse:
        """Update media."""
        data = request.data
        where = request.where
        include = request.include

        async with self._graphite.tx() as transaction:
            with self._handle_errors():
                old = await transaction.media.find_unique(
                    where=where,
                )

                if old is None:
                    return m.UpdateResponse(
                        media=None,
                    )

                new = await transaction.media.update(
                    data=cast("gt.MediaUpdateInput", data),
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
        self, transaction: GraphiteService, media: m.Media
    ) -> Sequence[m.Binding]:
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

            await self._minium.delete(req)
        except me.NotFoundError:
            pass

    async def delete(self, request: m.DeleteRequest) -> m.DeleteResponse:
        """Delete media."""
        where = request.where
        include = request.include

        async with self._graphite.tx() as transaction:
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
            media = await self._graphite.media.find_unique(
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

            await self._minium.upload(req)

        return m.UploadResponse(
            media=media,
        )

    async def download(self, request: m.DownloadRequest) -> m.DownloadResponse:
        """Download media content."""
        where = request.where
        include = request.include

        with self._handle_errors():
            media = await self._graphite.media.find_unique(
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

                res = await self._minium.download(req)

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
