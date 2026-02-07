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
        self, graphite: GraphiteService, minium: MiniumService, channels: ChannelsPlugin
    ) -> None:
        self._graphite = graphite
        self._minium = minium
        self._channels = channels

    def _emit_event(self, event: Event) -> None:
        data = event.model_dump_json(round_trip=True)
        self._channels.publish(data, "events")

    def _emit_media_created_event(self, media: m.Media) -> None:
        self._emit_event(
            mev.MediaCreatedEvent(
                data=mev.MediaCreatedEventData(media=mev.Media.map(media))
            )
        )

    def _emit_media_updated_event(self, media: m.Media) -> None:
        self._emit_event(
            mev.MediaUpdatedEvent(
                data=mev.MediaUpdatedEventData(media=mev.Media.map(media))
            )
        )

    def _emit_media_deleted_event(self, media: m.Media) -> None:
        self._emit_event(
            mev.MediaDeletedEvent(
                data=mev.MediaDeletedEventData(media=mev.Media.map(media))
            )
        )

    def _emit_binding_updated_event(self, binding: m.Binding) -> None:
        self._emit_event(
            bev.BindingUpdatedEvent(
                data=bev.BindingUpdatedEventData(binding=bev.Binding.map(binding))
            )
        )

    def _emit_binding_deleted_event(self, binding: m.Binding) -> None:
        self._emit_event(
            bev.BindingDeletedEvent(
                data=bev.BindingDeletedEventData(binding=bev.Binding.map(binding))
            )
        )

    @contextmanager
    def _handle_errors(self) -> Generator[None]:
        try:
            yield
        except ge.DataError as ex:
            raise e.ValidationError from ex
        except ge.ServiceError as ex:
            raise e.GraphiteError from ex
        except me.ServiceError as ex:
            raise e.MiniumError from ex

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

        self._emit_media_created_event(media)

        return m.CreateResponse(media=media)

    async def _update_handle_bindings(
        self, transaction: GraphiteService, old: m.Media, new: m.Media
    ) -> Sequence[m.Binding]:
        bindings = []

        if new.id != old.id:
            bindings = await transaction.binding.find_many(where={"mediaId": old.id})

            ids = [binding.id for binding in bindings]

            await transaction.binding.delete_many(where={"id": {"in": ids}})

            await transaction.binding.create_many(
                data=[
                    {
                        "id": binding.id,
                        "playlistId": binding.playlistId,
                        "mediaId": new.id,
                        "rank": binding.rank,
                    }
                    for binding in bindings
                ]
            )

            bindings = await transaction.binding.find_many(where={"id": {"in": ids}})

        return bindings

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

                bindings = await self._update_handle_bindings(transaction, old, new)
                await self._update_handle_content(old, new)

        self._emit_media_updated_event(new)
        for binding in bindings:
            self._emit_binding_updated_event(binding)

        return m.UpdateResponse(media=new)

    async def _delete_handle_bindings(
        self, transaction: GraphiteService, media: m.Media
    ) -> Sequence[m.Binding]:
        bindings = await transaction.binding.find_many(where={"mediaId": media.id})

        await transaction.binding.delete_many(
            where={"id": {"in": [binding.id for binding in bindings]}}
        )

        return bindings

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

                deleted = await self._delete_handle_bindings(transaction, media)
                await self._delete_handle_content(media)

        self._emit_media_deleted_event(media)
        for binding in deleted:
            self._emit_binding_deleted_event(binding)

        return m.DeleteResponse(media=media)

    async def upload(self, request: m.UploadRequest) -> m.UploadResponse:
        """Upload media content."""
        with self._handle_errors():
            media = await self._graphite.media.find_unique(
                where=request.where, include=request.include
            )

            if media is None:
                return m.UploadResponse(media=None)

            upload_request = mm.UploadRequest(name=media.id, content=request.content)
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

                content = download_response.content
            except me.NotFoundError:
                return m.DownloadResponse(media=media, content=None)

        return m.DownloadResponse(media=media, content=content)
