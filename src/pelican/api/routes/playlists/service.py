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
            raise e.ValidationError from ex
        except pe.GraphiteError as ex:
            raise e.GraphiteError from ex
        except pe.ServiceError as ex:
            raise e.ServiceError from ex

    async def list(self, request: m.ListRequest) -> m.ListResponse:
        """List playlists."""
        count_request = pm.CountRequest(where=request.where)

        with self._handle_errors():
            count_response = await self._playlists.count(count_request)

        list_request = pm.ListRequest(
            limit=request.limit,
            offset=request.offset,
            where=request.where,
            include=request.include,
            order=request.order,
        )

        with self._handle_errors():
            list_response = await self._playlists.list(list_request)

        return m.ListResponse(
            results=m.PlaylistList(
                count=count_response.count,
                limit=request.limit,
                offset=request.offset,
                playlists=[
                    m.Playlist.map(playlist) for playlist in list_response.playlists
                ],
            )
        )

    async def get(self, request: m.GetRequest) -> m.GetResponse:
        """Get playlist."""
        get_request = pm.GetRequest(
            where={"id": str(request.id)}, include=request.include
        )

        with self._handle_errors():
            get_response = await self._playlists.get(get_request)

        if get_response.playlist is None:
            raise e.PlaylistNotFoundError(request.id)

        return m.GetResponse(playlist=m.Playlist.map(get_response.playlist))

    async def create(self, request: m.CreateRequest) -> m.CreateResponse:
        """Create playlist."""
        create_request = pm.CreateRequest(data=request.data, include=request.include)

        with self._handle_errors():
            create_response = await self._playlists.create(create_request)

        return m.CreateResponse(playlist=m.Playlist.map(create_response.playlist))

    async def update(self, request: m.UpdateRequest) -> m.UpdateResponse:
        """Update playlist."""
        update_request = pm.UpdateRequest(
            data=request.data, where={"id": str(request.id)}, include=request.include
        )

        with self._handle_errors():
            update_response = await self._playlists.update(update_request)

        if update_response.playlist is None:
            raise e.PlaylistNotFoundError(request.id)

        return m.UpdateResponse(playlist=m.Playlist.map(update_response.playlist))

    async def delete(self, request: m.DeleteRequest) -> m.DeleteResponse:
        """Delete playlist."""
        delete_request = pm.DeleteRequest(where={"id": str(request.id)}, include=None)

        with self._handle_errors():
            delete_response = await self._playlists.delete(delete_request)

        if delete_response.playlist is None:
            raise e.PlaylistNotFoundError(request.id)

        return m.DeleteResponse()

    async def m3u(self, request: m.M3URequest) -> m.M3UResponse:
        """Get playlist in M3U format."""
        m3u_request = pm.M3URequest(where={"id": str(request.id)}, base=request.base)

        with self._handle_errors():
            m3u_response = await self._playlists.m3u(m3u_request)

        if m3u_response.m3u is None:
            raise e.PlaylistNotFoundError(request.id)

        return m.M3UResponse(m3u=m3u_response.m3u)

    async def headm3u(self, request: m.HeadM3URequest) -> m.HeadM3UResponse:
        """Get headers for playlist in M3U format."""
        m3u_request = pm.M3URequest(where={"id": str(request.id)}, base=request.base)

        with self._handle_errors():
            m3u_response = await self._playlists.m3u(m3u_request)

        if m3u_response.m3u is None:
            raise e.PlaylistNotFoundError(request.id)

        return m.HeadM3UResponse(m3u=m3u_response.m3u)
