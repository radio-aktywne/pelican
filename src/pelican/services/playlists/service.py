import builtins
from collections.abc import Generator, Sequence
from contextlib import contextmanager
from typing import cast

from litestar.channels import ChannelsPlugin

from pelican.models.events import bindings as bev
from pelican.models.events import playlists as pev
from pelican.models.events.types import Event
from pelican.services.graphite import errors as ge
from pelican.services.graphite import types as gt
from pelican.services.graphite.service import GraphiteService
from pelican.services.playlists import errors as e
from pelican.services.playlists import models as m
from pelican.utils.m3u import M3U


class PlaylistsService:
    """Service to manage playlists."""

    def __init__(self, graphite: GraphiteService, channels: ChannelsPlugin) -> None:
        self._graphite = graphite
        self._channels = channels

    def _emit_event(self, event: Event) -> None:
        data = event.model_dump_json(round_trip=True)
        self._channels.publish(data, "events")

    def _emit_playlist_created_event(self, playlist: m.Playlist) -> None:
        self._emit_event(
            pev.PlaylistCreatedEvent(
                data=pev.PlaylistCreatedEventData(playlist=pev.Playlist.map(playlist))
            )
        )

    def _emit_playlist_updated_event(self, playlist: m.Playlist) -> None:
        self._emit_event(
            pev.PlaylistUpdatedEvent(
                data=pev.PlaylistUpdatedEventData(playlist=pev.Playlist.map(playlist))
            )
        )

    def _emit_playlist_deleted_event(self, playlist: m.Playlist) -> None:
        self._emit_event(
            pev.PlaylistDeletedEvent(
                data=pev.PlaylistDeletedEventData(playlist=pev.Playlist.map(playlist))
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

    async def count(self, request: m.CountRequest) -> m.CountResponse:
        """Count playlists."""
        with self._handle_errors():
            count = await self._graphite.playlist.count(where=request.where)

        return m.CountResponse(count=count)

    async def list(self, request: m.ListRequest) -> m.ListResponse:
        """List all playlists."""
        with self._handle_errors():
            playlists = await self._graphite.playlist.find_many(
                take=request.limit,
                skip=request.offset,
                where=request.where,
                include=request.include,
                order=list(request.order)
                if isinstance(request.order, Sequence)
                else request.order,
            )

        return m.ListResponse(playlists=playlists)

    async def get(self, request: m.GetRequest) -> m.GetResponse:
        """Get playlist."""
        with self._handle_errors():
            playlist = await self._graphite.playlist.find_unique(
                where=request.where, include=request.include
            )

        return m.GetResponse(playlist=playlist)

    async def create(self, request: m.CreateRequest) -> m.CreateResponse:
        """Create playlist."""
        with self._handle_errors():
            playlist = await self._graphite.playlist.create(
                data=cast("gt.PlaylistCreateInput", request.data),
                include=request.include,
            )

        self._emit_playlist_created_event(playlist)

        return m.CreateResponse(playlist=playlist)

    async def _update_handle_bindings(
        self,
        transaction: GraphiteService,
        old: m.Playlist,
        new: m.Playlist,
    ) -> builtins.list[m.Binding]:
        bindings = []

        if new.id != old.id:
            bindings = await transaction.binding.find_many(where={"playlistId": old.id})

            ids = [binding.id for binding in bindings]

            await transaction.binding.delete_many(where={"id": {"in": ids}})

            await transaction.binding.create_many(
                data=[
                    {
                        "id": binding.id,
                        "playlistId": new.id,
                        "mediaId": binding.mediaId,
                        "rank": binding.rank,
                    }
                    for binding in bindings
                ]
            )

            bindings = await transaction.binding.find_many(where={"id": {"in": ids}})

        return bindings

    async def update(self, request: m.UpdateRequest) -> m.UpdateResponse:
        """Update playlist."""
        async with self._graphite.tx() as transaction:
            with self._handle_errors():
                old = await transaction.playlist.find_unique(where=request.where)

                if old is None:
                    return m.UpdateResponse(playlist=None)

                new = await transaction.playlist.update(
                    data=cast("gt.PlaylistUpdateInput", request.data),
                    where=request.where,
                    include=request.include,
                )

                if new is None:
                    return m.UpdateResponse(playlist=None)

                bindings = await self._update_handle_bindings(transaction, old, new)

        self._emit_playlist_updated_event(new)
        for binding in bindings:
            self._emit_binding_updated_event(binding)

        return m.UpdateResponse(playlist=new)

    async def _delete_handle_bindings(
        self,
        transaction: GraphiteService,
        playlist: m.Playlist,
    ) -> builtins.list[m.Binding]:
        bindings = await transaction.binding.find_many(
            where={"playlistId": playlist.id}
        )

        await transaction.binding.delete_many(
            where={"id": {"in": [binding.id for binding in bindings]}}
        )

        return bindings

    async def delete(self, request: m.DeleteRequest) -> m.DeleteResponse:
        """Delete playlist."""
        async with self._graphite.tx() as transaction:
            with self._handle_errors():
                playlist = await transaction.playlist.delete(
                    where=request.where, include=request.include
                )

                if playlist is None:
                    return m.DeleteResponse(playlist=None)

                bindings = await self._delete_handle_bindings(transaction, playlist)

        self._emit_playlist_deleted_event(playlist)
        for binding in bindings:
            self._emit_binding_deleted_event(binding)

        return m.DeleteResponse(playlist=playlist)

    async def m3u(self, request: m.M3URequest) -> m.M3UResponse:
        """Get playlist in M3U format."""
        with self._handle_errors():
            playlist = await self._graphite.playlist.find_unique(
                where=request.where, include={"bindings": {"order_by": {"rank": "asc"}}}
            )

        if playlist is None:
            return m.M3UResponse(m3u=None)

        urls = [
            f"{request.base.rstrip('/')}/media/{binding.mediaId}/content"
            for binding in playlist.bindings or []
        ]

        return m.M3UResponse(m3u=str(M3U(urls)))
