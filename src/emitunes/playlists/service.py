from litestar.channels import ChannelsPlugin

from emitunes.datatunes import errors as de
from emitunes.datatunes.service import DatatunesService
from emitunes.models import events as ev
from emitunes.playlists import errors as e
from emitunes.playlists import models as m


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

    def _emit_created_event(self, playlist: m.Playlist) -> None:
        """Emit a playlist created event."""

        data = ev.PlaylistCreatedEventData(
            playlist=playlist,
        )
        event = ev.PlaylistCreatedEvent(
            data=data,
        )
        self._emit_event(event)

    def _emit_updated_event(self, playlist: m.Playlist) -> None:
        """Emit a playlist updated event."""

        data = ev.PlaylistUpdatedEventData(
            playlist=playlist,
        )
        event = ev.PlaylistUpdatedEvent(
            data=data,
        )
        self._emit_event(event)

    def _emit_deleted_event(self, playlist: m.Playlist) -> None:
        """Emit a playlist deleted event."""

        data = ev.PlaylistDeletedEventData(
            playlist=playlist,
        )
        event = ev.PlaylistDeletedEvent(
            data=data,
        )
        self._emit_event(event)

    async def count(self, request: m.CountRequest) -> m.CountResponse:
        """Count playlists."""

        where = request.where

        try:
            count = await self._datatunes.playlist.count(
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
        """List all playlists."""

        limit = request.limit
        offset = request.offset
        where = request.where
        include = request.include
        order = request.order

        try:
            playlists = await self._datatunes.playlist.find_many(
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
            playlists=playlists,
        )

    async def get(self, request: m.GetRequest) -> m.GetResponse:
        """Get playlist."""

        where = request.where
        include = request.include

        try:
            playlist = await self._datatunes.playlist.find_unique(
                where=where,
                include=include,
            )
        except de.DataError as ex:
            raise e.ValidationError(str(ex)) from ex
        except de.DatatunesError as ex:
            raise e.DatatunesError(str(ex)) from ex

        return m.GetResponse(
            playlist=playlist,
        )

    async def create(self, request: m.CreateRequest) -> m.CreateResponse:
        """Create playlist."""

        data = request.data
        include = request.include

        try:
            playlist = await self._datatunes.playlist.create(
                data=data,
                include=include,
            )
        except de.DataError as ex:
            raise e.ValidationError(str(ex)) from ex
        except de.DatatunesError as ex:
            raise e.DatatunesError(str(ex)) from ex

        self._emit_created_event(playlist)

        return m.CreateResponse(
            playlist=playlist,
        )

    async def update(self, request: m.UpdateRequest) -> m.UpdateResponse:
        """Update playlist."""

        data = request.data
        where = request.where
        include = request.include

        async with self._datatunes.tx() as transaction:
            try:
                playlist = await transaction.playlist.update(
                    data=data,
                    where=where,
                    include=include,
                )
            except de.DataError as ex:
                raise e.ValidationError(str(ex)) from ex
            except de.DatatunesError as ex:
                raise e.DatatunesError(str(ex)) from ex

            if playlist is None:
                return m.UpdateResponse(playlist=None)

        self._emit_updated_event(playlist)

        return m.UpdateResponse(
            playlist=playlist,
        )

    async def delete(self, request: m.DeleteRequest) -> m.DeleteResponse:
        """Delete playlist."""

        where = request.where
        include = request.include

        async with self._datatunes.tx() as transaction:
            try:
                playlist = await transaction.playlist.delete(
                    where=where,
                    include=include,
                )
            except de.DataError as ex:
                raise e.ValidationError(str(ex)) from ex
            except de.DatatunesError as ex:
                raise e.DatatunesError(str(ex)) from ex

            if playlist is None:
                return m.DeleteResponse(playlist=None)

        self._emit_deleted_event(playlist)

        return m.DeleteResponse(
            playlist=playlist,
        )
