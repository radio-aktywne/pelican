from typing import Annotated

from litestar import Controller as BaseController
from litestar import Request, handlers
from litestar.channels import ChannelsPlugin
from litestar.datastructures import ResponseHeader
from litestar.di import Provide
from litestar.params import Body, Parameter
from litestar.response import Response

from emitunes.api.exceptions import BadRequestException, NotFoundException
from emitunes.api.routes.playlists import errors as e
from emitunes.api.routes.playlists import models as m
from emitunes.api.routes.playlists.service import Service
from emitunes.api.validator import Validator
from emitunes.services.playlists.service import PlaylistsService
from emitunes.state import State


class DependenciesBuilder:
    """Builder for the dependencies of the controller."""

    async def _build_service(
        self,
        state: State,
        channels: ChannelsPlugin,
    ) -> Service:
        return Service(
            playlists=PlaylistsService(
                datatunes=state.datatunes,
                channels=channels,
            )
        )

    def build(self) -> dict[str, Provide]:
        return {
            "service": Provide(self._build_service),
        }


class Controller(BaseController):
    """Controller for the playlists endpoint."""

    dependencies = DependenciesBuilder().build()

    @handlers.get(
        summary="List playlists",
    )
    async def list(
        self,
        service: Service,
        limit: Annotated[
            m.ListRequestLimit,
            Parameter(
                description="Maximum number of playlists to return.",
            ),
        ] = 10,
        offset: Annotated[
            m.ListRequestOffset,
            Parameter(
                description="Number of playlists to skip.",
            ),
        ] = None,
        where: Annotated[
            str | None,
            Parameter(
                description="Filter to apply to find playlists.",
            ),
        ] = None,
        include: Annotated[
            str | None,
            Parameter(
                description="Relations to include in the response.",
            ),
        ] = None,
        order: Annotated[
            str | None,
            Parameter(
                description="Order to apply to the results.",
            ),
        ] = None,
    ) -> Response[m.ListResponseResults]:
        """List playlists that match the request."""

        where = Validator(m.ListRequestWhere).json(where) if where else None
        include = Validator(m.ListRequestInclude).json(include) if include else None
        order = Validator(m.ListRequestOrder).json(order) if order else None

        req = m.ListRequest(
            limit=limit,
            offset=offset,
            where=where,
            include=include,
            order=order,
        )

        try:
            res = await service.list(req)
        except e.ValidationError as ex:
            raise BadRequestException(extra=str(ex)) from ex

        results = res.results

        return Response(results)

    @handlers.get(
        "/{id:uuid}",
        summary="Get playlist",
    )
    async def get(
        self,
        service: Service,
        id: Annotated[
            m.GetRequestId,
            Parameter(
                description="Identifier of the playlist to get.",
            ),
        ],
        include: Annotated[
            str | None,
            Parameter(
                description="Relations to include in the response.",
            ),
        ] = None,
    ) -> Response[m.GetResponsePlaylist]:
        """Get a playlist by ID."""

        include = Validator(m.GetRequestInclude).json(include) if include else None

        req = m.GetRequest(
            id=id,
            include=include,
        )

        try:
            res = await service.get(req)
        except e.ValidationError as ex:
            raise BadRequestException(extra=str(ex)) from ex
        except e.PlaylistNotFoundError as ex:
            raise NotFoundException(extra=str(ex)) from ex

        playlist = res.playlist

        return Response(playlist)

    @handlers.post(
        summary="Create playlist",
    )
    async def create(
        self,
        service: Service,
        data: Annotated[
            m.CreateRequestData,
            Body(
                description="Data to create a playlist.",
            ),
        ],
        include: Annotated[
            str | None,
            Parameter(
                description="Relations to include in the response.",
            ),
        ] = None,
    ) -> Response[m.CreateResponsePlaylist]:
        """Create a new playlist."""

        data = Validator(m.CreateRequestData).object(data)
        include = Validator(m.CreateRequestInclude).json(include) if include else None

        req = m.CreateRequest(
            data=data,
            include=include,
        )

        try:
            res = await service.create(req)
        except e.ValidationError as ex:
            raise BadRequestException(extra=str(ex)) from ex

        playlist = res.playlist

        return Response(playlist)

    @handlers.patch(
        "/{id:uuid}",
        summary="Update playlist",
    )
    async def update(
        self,
        service: Service,
        id: Annotated[
            m.UpdateRequestId,
            Parameter(
                description="Identifier of the playlist to update.",
            ),
        ],
        data: Annotated[
            m.UpdateRequestData,
            Body(
                description="Data to update a playlist.",
            ),
        ],
        include: Annotated[
            str | None,
            Parameter(
                description="Relations to include in the response.",
            ),
        ] = None,
    ) -> Response[m.UpdateResponsePlaylist]:
        """Update a playlist by ID."""

        data = Validator(m.UpdateRequestData).object(data)
        include = Validator(m.UpdateRequestInclude).json(include) if include else None

        req = m.UpdateRequest(
            data=data,
            id=id,
            include=include,
        )

        try:
            res = await service.update(req)
        except e.ValidationError as ex:
            raise BadRequestException(extra=str(ex)) from ex
        except e.PlaylistNotFoundError as ex:
            raise NotFoundException(extra=str(ex)) from ex

        playlist = res.playlist

        return Response(playlist)

    @handlers.delete(
        "/{id:uuid}",
        summary="Delete playlist",
    )
    async def delete(
        self,
        service: Service,
        id: Annotated[
            m.DeleteRequestId,
            Parameter(
                description="Identifier of the playlist to delete.",
            ),
        ],
    ) -> Response[None]:
        """Delete a playlist by ID."""

        req = m.DeleteRequest(
            id=id,
        )

        try:
            await service.delete(req)
        except e.ValidationError as ex:
            raise BadRequestException(extra=str(ex)) from ex
        except e.PlaylistNotFoundError as ex:
            raise NotFoundException(extra=str(ex)) from ex

        return Response(None)

    @handlers.get(
        "/{id:uuid}/m3u",
        summary="Get playlist in M3U format",
        media_type="audio/mpegurl",
        response_headers=[
            ResponseHeader(
                name="Content-Type",
                description="Content type.",
                value="audio/mpegurl",
            ),
        ],
    )
    async def m3u(
        self,
        service: Service,
        id: Annotated[
            m.M3URequestId,
            Parameter(
                description="Identifier of the playlist to get.",
            ),
        ],
        request: Request,
    ) -> Response[m.M3UResponseM3U]:
        """Get a playlist in M3U format."""

        req = m.M3URequest(
            id=id,
            base=str(request.base_url),
        )

        try:
            res = await service.m3u(req)
        except e.ValidationError as ex:
            raise BadRequestException(extra=str(ex)) from ex
        except e.PlaylistNotFoundError as ex:
            raise NotFoundException(extra=str(ex)) from ex

        m3u = res.m3u

        return Response(m3u)

    @handlers.head(
        "/{id:uuid}/m3u",
        summary="Get headers for playlist in M3U format",
        response_headers=[
            ResponseHeader(
                name="Content-Type",
                description="Content type.",
                value="audio/mpegurl",
            ),
        ],
    )
    async def headm3u(
        self,
        service: Service,
        id: Annotated[
            m.HeadM3URequestId,
            Parameter(
                description="Identifier of the playlist to get.",
            ),
        ],
        request: Request,
    ) -> Response[None]:
        """Get headers for a playlist in M3U format."""

        req = m.HeadM3URequest(
            id=id,
            base=str(request.base_url),
        )

        try:
            await service.headm3u(req)
        except e.ValidationError as ex:
            raise BadRequestException(extra=str(ex)) from ex
        except e.PlaylistNotFoundError as ex:
            raise NotFoundException(extra=str(ex)) from ex

        return Response(None)
