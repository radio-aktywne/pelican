from collections.abc import Mapping
from typing import Annotated

from litestar import Controller as BaseController
from litestar import Request, handlers
from litestar.channels import ChannelsPlugin
from litestar.datastructures import ResponseHeader
from litestar.di import Provide
from litestar.openapi import ResponseSpec
from litestar.params import Body, Parameter
from litestar.response import Response
from litestar.status_codes import HTTP_200_OK, HTTP_204_NO_CONTENT

from pelican.api.exceptions import BadRequestException, NotFoundException
from pelican.api.routes.playlists import errors as e
from pelican.api.routes.playlists import models as m
from pelican.api.routes.playlists.service import Service
from pelican.models.base import Jsonable, Serializable
from pelican.services.playlists.service import PlaylistsService
from pelican.state import State


class DependenciesBuilder:
    """Builder for the dependencies of the controller."""

    async def _build_service(self, state: State, channels: ChannelsPlugin) -> Service:
        return Service(
            playlists=PlaylistsService(graphite=state.graphite, channels=channels)
        )

    def build(self) -> Mapping[str, Provide]:
        """Build the dependencies."""
        return {
            "service": Provide(self._build_service),
        }


class Controller(BaseController):
    """Controller for the playlists endpoint."""

    dependencies = DependenciesBuilder().build()

    @handlers.get(
        summary="List playlists",
    )
    async def list(  # noqa: PLR0913
        self,
        service: Service,
        limit: Annotated[
            Jsonable[m.ListRequestLimit] | None,
            Parameter(
                description="Maximum number of playlists to return. Default is 10.",
            ),
        ] = None,
        offset: Annotated[
            Jsonable[m.ListRequestOffset] | None,
            Parameter(
                description="Number of playlists to skip.",
            ),
        ] = None,
        where: Annotated[
            Jsonable[m.ListRequestWhere] | None,
            Parameter(
                description="Filter to apply to find playlists.",
            ),
        ] = None,
        include: Annotated[
            Jsonable[m.ListRequestInclude] | None,
            Parameter(
                description="Relations to include in the response.",
            ),
        ] = None,
        order: Annotated[
            Jsonable[m.ListRequestOrder] | None,
            Parameter(
                description="Order to apply to the results.",
            ),
        ] = None,
    ) -> Response[Serializable[m.ListResponseResults]]:
        """List playlists that match the request."""
        request = m.ListRequest(
            limit=limit.root if limit else 10,
            offset=offset.root if offset else None,
            where=where.root if where else None,
            include=include.root if include else None,
            order=order.root if order else None,
        )

        try:
            response = await service.list(request)
        except e.ValidationError as ex:
            raise BadRequestException from ex

        return Response(Serializable(response.results))

    @handlers.get(
        "/{id:str}",
        summary="Get playlist",
    )
    async def get(
        self,
        service: Service,
        id: Annotated[  # noqa: A002
            Serializable[m.GetRequestId],
            Parameter(
                description="Identifier of the playlist to get.",
            ),
        ],
        include: Annotated[
            Jsonable[m.GetRequestInclude] | None,
            Parameter(
                description="Relations to include in the response.",
            ),
        ] = None,
    ) -> Response[Serializable[m.GetResponsePlaylist]]:
        """Get a playlist by ID."""
        request = m.GetRequest(id=id.root, include=include.root if include else None)

        try:
            response = await service.get(request)
        except e.ValidationError as ex:
            raise BadRequestException from ex
        except e.PlaylistNotFoundError as ex:
            raise NotFoundException from ex

        return Response(Serializable(response.playlist))

    @handlers.post(
        summary="Create playlist",
    )
    async def create(
        self,
        service: Service,
        data: Annotated[
            Serializable[m.CreateRequestData],
            Body(
                description="Data to create a playlist.",
            ),
        ],
        include: Annotated[
            Jsonable[m.CreateRequestInclude] | None,
            Parameter(
                description="Relations to include in the response.",
            ),
        ] = None,
    ) -> Response[Serializable[m.CreateResponsePlaylist]]:
        """Create a new playlist."""
        request = m.CreateRequest(
            data=data.root, include=include.root if include else None
        )

        try:
            response = await service.create(request)
        except e.ValidationError as ex:
            raise BadRequestException from ex

        return Response(Serializable(response.playlist))

    @handlers.patch(
        "/{id:str}",
        summary="Update playlist",
    )
    async def update(
        self,
        service: Service,
        id: Annotated[  # noqa: A002
            Serializable[m.UpdateRequestId],
            Parameter(
                description="Identifier of the playlist to update.",
            ),
        ],
        data: Annotated[
            Serializable[m.UpdateRequestData],
            Body(
                description="Data to update a playlist.",
            ),
        ],
        include: Annotated[
            Jsonable[m.UpdateRequestInclude] | None,
            Parameter(
                description="Relations to include in the response.",
            ),
        ] = None,
    ) -> Response[Serializable[m.UpdateResponsePlaylist]]:
        """Update a playlist by ID."""
        request = m.UpdateRequest(
            data=data.root,
            id=id.root,
            include=include.root if include else None,
        )

        try:
            response = await service.update(request)
        except e.ValidationError as ex:
            raise BadRequestException from ex
        except e.PlaylistNotFoundError as ex:
            raise NotFoundException from ex

        return Response(Serializable(response.playlist))

    @handlers.delete(
        "/{id:str}",
        summary="Delete playlist",
        responses={
            HTTP_204_NO_CONTENT: ResponseSpec(
                None, description="Request fulfilled, nothing follows"
            )
        },
    )
    async def delete(
        self,
        service: Service,
        id: Annotated[  # noqa: A002
            Serializable[m.DeleteRequestId],
            Parameter(
                description="Identifier of the playlist to delete.",
            ),
        ],
    ) -> Response[None]:
        """Delete a playlist by ID."""
        request = m.DeleteRequest(id=id.root)

        try:
            await service.delete(request)
        except e.ValidationError as ex:
            raise BadRequestException from ex
        except e.PlaylistNotFoundError as ex:
            raise NotFoundException from ex

        return Response(None)

    @handlers.get(
        "/{id:str}/m3u",
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
        id: Annotated[  # noqa: A002
            Serializable[m.M3URequestId],
            Parameter(
                description="Identifier of the playlist to get.",
            ),
        ],
        request: Request,
    ) -> Response[m.M3UResponseM3U]:
        """Get a playlist in M3U format."""
        req = m.M3URequest(id=id.root, base=str(request.base_url))

        try:
            response = await service.m3u(req)
        except e.ValidationError as ex:
            raise BadRequestException from ex
        except e.PlaylistNotFoundError as ex:
            raise NotFoundException from ex

        return Response(response.m3u)

    @handlers.head(
        "/{id:str}/m3u",
        summary="Get headers for playlist in M3U format",
        response_headers=[
            ResponseHeader(
                name="Content-Type",
                description="Content type.",
                value="audio/mpegurl",
            ),
        ],
        responses={
            HTTP_200_OK: ResponseSpec(
                None, description="Request fulfilled, nothing follows"
            )
        },
    )
    async def headm3u(
        self,
        service: Service,
        id: Annotated[  # noqa: A002
            Serializable[m.HeadM3URequestId],
            Parameter(
                description="Identifier of the playlist to get.",
            ),
        ],
        request: Request,
    ) -> Response[None]:
        """Get headers for a playlist in M3U format."""
        req = m.HeadM3URequest(id=id.root, base=str(request.base_url))

        try:
            await service.headm3u(req)
        except e.ValidationError as ex:
            raise BadRequestException from ex
        except e.PlaylistNotFoundError as ex:
            raise NotFoundException from ex

        return Response(None)
