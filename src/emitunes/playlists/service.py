import builtins
from collections.abc import Generator
from contextlib import contextmanager

from litestar.channels import ChannelsPlugin

from emitunes.bindings import models as bm
from emitunes.datatunes import errors as de
from emitunes.datatunes.service import DatatunesService
from emitunes.models import events as ev
from emitunes.playlists import errors as e
from emitunes.playlists import models as m
from emitunes.utils.m3u import M3U


class PlaylistsService:
    """Service to manage playlists."""

    def __init__(
        self,
        datatunes: DatatunesService,
        channels: ChannelsPlugin,
    ) -> None:
        self._datatunes = datatunes
        self._channels = channels

    def _emit_event(self, event: ev.Event) -> None:
        """Emit an event."""

        data = event.model_dump_json(by_alias=True)
        self._channels.publish(data, "events")

    def _emit_playlist_created_event(self, playlist: m.Playlist) -> None:
        """Emit a playlist created event."""

        data = ev.PlaylistCreatedEventData(
            playlist=playlist,
        )
        event = ev.PlaylistCreatedEvent(
            data=data,
        )
        self._emit_event(event)

    def _emit_playlist_updated_event(self, playlist: m.Playlist) -> None:
        """Emit a playlist updated event."""

        data = ev.PlaylistUpdatedEventData(
            playlist=playlist,
        )
        event = ev.PlaylistUpdatedEvent(
            data=data,
        )
        self._emit_event(event)

    def _emit_playlist_deleted_event(self, playlist: m.Playlist) -> None:
        """Emit a playlist deleted event."""

        data = ev.PlaylistDeletedEventData(
            playlist=playlist,
        )
        event = ev.PlaylistDeletedEvent(
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

    async def count(self, request: m.CountRequest) -> m.CountResponse:
        """Count playlists."""

        where = request.where

        with self._handle_errors():
            count = await self._datatunes.playlist.count(
                where=where,
            )

        return m.CountResponse(
            count=count,
        )

    async def list(self, request: m.ListRequest) -> m.ListResponse:
        """List all playlists."""

        limit = request.limit
        offset = request.offset
        where = request.where
        include = request.include
        order = request.order

        with self._handle_errors():
            playlists = await self._datatunes.playlist.find_many(
                take=limit,
                skip=offset,
                where=where,
                include=include,
                order=order,
            )

        return m.ListResponse(
            playlists=playlists,
        )

    async def get(self, request: m.GetRequest) -> m.GetResponse:
        """Get playlist."""

        where = request.where
        include = request.include

        with self._handle_errors():
            playlist = await self._datatunes.playlist.find_unique(
                where=where,
                include=include,
            )

        return m.GetResponse(
            playlist=playlist,
        )

    async def create(self, request: m.CreateRequest) -> m.CreateResponse:
        """Create playlist."""

        data = request.data
        include = request.include

        with self._handle_errors():
            playlist = await self._datatunes.playlist.create(
                data=data,
                include=include,
            )

        self._emit_playlist_created_event(playlist)

        return m.CreateResponse(
            playlist=playlist,
        )

    async def _update_handle_bindings(
        self,
        transaction: DatatunesService,
        old: m.Playlist,
        new: m.Playlist,
    ) -> builtins.list[bm.Binding]:
        bindings = []

        if new.id != old.id:
            bindings = await transaction.binding.find_many(
                where={"playlistId": old.id},
            )

            ids = [binding.id for binding in bindings]

            await transaction.binding.delete_many(
                where={"id": {"in": ids}},
            )

            await transaction.binding.create_many(
                data=[
                    {
                        "id": binding.id,
                        "playlistId": new.id,
                        "mediaId": binding.mediaId,
                        "rank": binding.rank,
                    }
                    for binding in bindings
                ],
            )

            bindings = await transaction.binding.find_many(
                where={"id": {"in": ids}},
            )

        return bindings

    async def update(self, request: m.UpdateRequest) -> m.UpdateResponse:
        """Update playlist."""

        data = request.data
        where = request.where
        include = request.include

        async with self._datatunes.tx() as transaction:
            with self._handle_errors():
                old = await transaction.playlist.find_unique(
                    where=where,
                )

                if old is None:
                    return m.UpdateResponse(playlist=None)

                new = await transaction.playlist.update(
                    data=data,
                    where=where,
                    include=include,
                )

                if new is None:
                    return m.UpdateResponse(playlist=None)

                bindings = await self._update_handle_bindings(transaction, old, new)

        self._emit_playlist_updated_event(new)
        for binding in bindings:
            self._emit_binding_updated_event(binding)

        return m.UpdateResponse(
            playlist=new,
        )

    async def _delete_handle_bindings(
        self,
        transaction: DatatunesService,
        playlist: m.Playlist,
    ) -> builtins.list[bm.Binding]:
        bindings = await transaction.binding.find_many(
            where={"playlistId": playlist.id},
        )

        await transaction.binding.delete_many(
            where={"id": {"in": [binding.id for binding in bindings]}},
        )

        return bindings

    async def delete(self, request: m.DeleteRequest) -> m.DeleteResponse:
        """Delete playlist."""

        where = request.where
        include = request.include

        async with self._datatunes.tx() as transaction:
            with self._handle_errors():
                playlist = await transaction.playlist.delete(
                    where=where,
                    include=include,
                )

                if playlist is None:
                    return m.DeleteResponse(playlist=None)

                bindings = await self._delete_handle_bindings(transaction, playlist)

        self._emit_playlist_deleted_event(playlist)
        for binding in bindings:
            self._emit_binding_deleted_event(binding)

        return m.DeleteResponse(
            playlist=playlist,
        )

    async def m3u(self, request: m.M3URequest) -> m.M3UResponse:
        """Get playlist in M3U format."""

        where = request.where
        base = request.base

        with self._handle_errors():
            playlist = await self._datatunes.playlist.find_unique(
                where=where,
                include={"bindings": {"order_by": {"rank": "asc"}}},
            )

        if playlist is None:
            return m.M3UResponse(
                m3u=None,
            )

        base = base.rstrip("/")
        urls = [
            f"{base}/media/{binding.mediaId}/content" for binding in playlist.bindings
        ]

        m3u = M3U(urls)
        m3u = str(m3u)

        return m.M3UResponse(
            m3u=m3u,
        )
