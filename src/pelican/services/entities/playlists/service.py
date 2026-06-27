from collections.abc import Generator, Sequence
from contextlib import contextmanager
from typing import cast

from pelican.services.data.graphite import errors as ge
from pelican.services.data.graphite import types as gt
from pelican.services.data.graphite.service import GraphiteService
from pelican.services.entities.playlists import errors as e
from pelican.services.entities.playlists import models as m
from pelican.utils.m3u import M3U


class PlaylistsService:
    """Service to manage playlists."""

    def __init__(self, graphite: GraphiteService) -> None:
        self._graphite = graphite

    @contextmanager
    def _handle_errors(self) -> Generator[None]:
        try:
            yield
        except ge.UniqueViolationError as ex:
            raise e.ConflictError from ex
        except ge.DataError as ex:
            raise e.ValidationError from ex
        except ge.ServiceError as ex:
            raise e.ServiceError from ex

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

        return m.CreateResponse(playlist=playlist)

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

        return m.UpdateResponse(playlist=new)

    async def delete(self, request: m.DeleteRequest) -> m.DeleteResponse:
        """Delete playlist."""
        async with self._graphite.tx() as transaction:
            with self._handle_errors():
                playlist = await transaction.playlist.delete(
                    where=request.where, include=request.include
                )

                if playlist is None:
                    return m.DeleteResponse(playlist=None)

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
