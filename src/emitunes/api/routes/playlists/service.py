from collections.abc import Generator
from contextlib import contextmanager

from emitunes.api.routes.playlists import errors as e
from emitunes.api.routes.playlists import models as m
from emitunes.playlists import errors as pe
from emitunes.playlists import models as pm
from emitunes.playlists.service import PlaylistsService


class Service:
    """Service for the playlists endpoint."""

    def __init__(self, playlists: PlaylistsService) -> None:
        self._playlists = playlists

    @contextmanager
    def _handle_errors(self) -> Generator[None, None, None]:
        try:
            yield
        except pe.ValidationError as ex:
            raise e.ValidationError(ex.message) from ex
        except pe.DatatunesError as ex:
            raise e.DatatunesError(ex.message) from ex
        except pe.ServiceError as ex:
            raise e.ServiceError(ex.message) from ex

    async def list(self, request: m.ListRequest) -> m.ListResponse:
        """List playlists."""

        limit = request.limit
        offset = request.offset
        where = request.where
        include = request.include
        order = request.order

        with self._handle_errors():
            response = await self._playlists.count(
                pm.CountRequest(
                    where=where,
                )
            )

        count = response.count

        with self._handle_errors():
            response = await self._playlists.list(
                pm.ListRequest(
                    limit=limit,
                    offset=offset,
                    where=where,
                    include=include,
                    order=order,
                )
            )

        playlists = response.playlists

        results = m.ListResponseResults(
            count=count,
            limit=limit,
            offset=offset,
            playlists=playlists,
        )
        return m.ListResponse(
            results=results,
        )

    async def get(self, request: m.GetRequest) -> m.GetResponse:
        """Get playlist."""

        id = request.id
        include = request.include

        with self._handle_errors():
            response = await self._playlists.get(
                pm.GetRequest(
                    where={
                        "id": str(id),
                    },
                    include=include,
                )
            )

        playlist = response.playlist

        if playlist is None:
            raise e.PlaylistNotFoundError(id)

        return m.GetResponse(
            playlist=playlist,
        )

    async def create(self, request: m.CreateRequest) -> m.CreateResponse:
        """Create playlist."""

        data = request.data
        include = request.include

        with self._handle_errors():
            response = await self._playlists.create(
                pm.CreateRequest(
                    data=data,
                    include=include,
                )
            )

        playlist = response.playlist

        return m.CreateResponse(
            playlist=playlist,
        )

    async def update(self, request: m.UpdateRequest) -> m.UpdateResponse:
        """Update playlist."""

        data = request.data
        id = request.id
        include = request.include

        with self._handle_errors():
            response = await self._playlists.update(
                pm.UpdateRequest(
                    data=data,
                    where={
                        "id": str(id),
                    },
                    include=include,
                )
            )

        playlist = response.playlist

        if playlist is None:
            raise e.PlaylistNotFoundError(id)

        return m.UpdateResponse(
            playlist=playlist,
        )

    async def delete(self, request: m.DeleteRequest) -> m.DeleteResponse:
        """Delete playlist."""

        id = request.id

        with self._handle_errors():
            response = await self._playlists.delete(
                pm.DeleteRequest(
                    where={
                        "id": str(id),
                    },
                )
            )

        playlist = response.playlist

        if playlist is None:
            raise e.PlaylistNotFoundError(id)

        return m.DeleteResponse()

    async def m3u(self, request: m.M3URequest) -> m.M3UResponse:
        """Get playlist in M3U format."""

        id = request.id
        base = request.base

        with self._handle_errors():
            response = await self._playlists.m3u(
                pm.M3URequest(
                    where={
                        "id": str(id),
                    },
                    base=base,
                )
            )

        m3u = response.m3u

        if m3u is None:
            raise e.PlaylistNotFoundError(id)

        return m.M3UResponse(
            m3u=m3u,
        )
