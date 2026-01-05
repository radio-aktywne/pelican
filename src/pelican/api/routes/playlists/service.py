from collections.abc import Generator
from contextlib import contextmanager

from pelican.api.routes.playlists import errors as e
from pelican.api.routes.playlists import models as m
from pelican.services.playlists import errors as pe
from pelican.services.playlists import models as pm
from pelican.services.playlists.service import PlaylistsService


class Service:
    """Service for the playlists endpoint."""

    def __init__(self, playlists: PlaylistsService) -> None:
        self._playlists = playlists

    @contextmanager
    def _handle_errors(self) -> Generator[None]:
        try:
            yield
        except pe.ValidationError as ex:
            raise e.ValidationError(str(ex)) from ex
        except pe.GraphiteError as ex:
            raise e.GraphiteError(str(ex)) from ex
        except pe.ServiceError as ex:
            raise e.ServiceError(str(ex)) from ex

    async def list(self, request: m.ListRequest) -> m.ListResponse:
        """List playlists."""
        limit = request.limit
        offset = request.offset
        where = request.where
        include = request.include
        order = request.order

        req = pm.CountRequest(
            where=where,
        )

        with self._handle_errors():
            res = await self._playlists.count(req)

        count = res.count

        req = pm.ListRequest(
            limit=limit,
            offset=offset,
            where=where,
            include=include,
            order=order,
        )

        with self._handle_errors():
            res = await self._playlists.list(req)

        playlists = res.playlists

        playlists = [m.Playlist.map(p) for p in playlists]
        results = m.PlaylistList(
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
        playlist_id = request.id
        include = request.include

        req = pm.GetRequest(
            where={
                "id": str(playlist_id),
            },
            include=include,
        )

        with self._handle_errors():
            res = await self._playlists.get(req)

        playlist = res.playlist

        if playlist is None:
            raise e.PlaylistNotFoundError(playlist_id)

        playlist = m.Playlist.map(playlist)
        return m.GetResponse(
            playlist=playlist,
        )

    async def create(self, request: m.CreateRequest) -> m.CreateResponse:
        """Create playlist."""
        data = request.data
        include = request.include

        req = pm.CreateRequest(
            data=data,
            include=include,
        )

        with self._handle_errors():
            res = await self._playlists.create(req)

        playlist = res.playlist

        playlist = m.Playlist.map(playlist)
        return m.CreateResponse(
            playlist=playlist,
        )

    async def update(self, request: m.UpdateRequest) -> m.UpdateResponse:
        """Update playlist."""
        data = request.data
        playlist_id = request.id
        include = request.include

        req = pm.UpdateRequest(
            data=data,
            where={
                "id": str(playlist_id),
            },
            include=include,
        )

        with self._handle_errors():
            res = await self._playlists.update(req)

        playlist = res.playlist

        if playlist is None:
            raise e.PlaylistNotFoundError(playlist_id)

        playlist = m.Playlist.map(playlist)
        return m.UpdateResponse(
            playlist=playlist,
        )

    async def delete(self, request: m.DeleteRequest) -> m.DeleteResponse:
        """Delete playlist."""
        playlist_id = request.id

        req = pm.DeleteRequest(
            where={
                "id": str(playlist_id),
            },
            include=None,
        )

        with self._handle_errors():
            res = await self._playlists.delete(req)

        playlist = res.playlist

        if playlist is None:
            raise e.PlaylistNotFoundError(playlist_id)

        return m.DeleteResponse()

    async def m3u(self, request: m.M3URequest) -> m.M3UResponse:
        """Get playlist in M3U format."""
        playlist_id = request.id
        base = request.base

        req = pm.M3URequest(
            where={
                "id": str(playlist_id),
            },
            base=base,
        )

        with self._handle_errors():
            res = await self._playlists.m3u(req)

        m3u = res.m3u

        if m3u is None:
            raise e.PlaylistNotFoundError(playlist_id)

        return m.M3UResponse(
            m3u=m3u,
        )

    async def headm3u(self, request: m.HeadM3URequest) -> m.HeadM3UResponse:
        """Get headers for playlist in M3U format."""
        playlist_id = request.id
        base = request.base

        req = pm.M3URequest(
            where={
                "id": str(playlist_id),
            },
            base=base,
        )

        with self._handle_errors():
            res = await self._playlists.m3u(req)

        m3u = res.m3u

        if m3u is None:
            raise e.PlaylistNotFoundError(playlist_id)

        return m.HeadM3UResponse(
            m3u=m3u,
        )
