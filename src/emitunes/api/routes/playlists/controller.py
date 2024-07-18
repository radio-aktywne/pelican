from typing import Annotated, TypeVar

from litestar import Controller as BaseController
from litestar import handlers
from litestar.channels import ChannelsPlugin
from litestar.di import Provide
from litestar.params import Parameter
from litestar.response import Response
from pydantic import Json, TypeAdapter
from pydantic import ValidationError as PydanticValidationError

from emitunes.api.exceptions import BadRequestException, NotFoundException
from emitunes.api.routes.playlists import errors as e
from emitunes.api.routes.playlists import models as m
from emitunes.api.routes.playlists.service import Service
from emitunes.playlists.service import PlaylistsService
from emitunes.state import State

T = TypeVar("T")


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

    def _validate_pydantic(self, t: type[T], v: str) -> T:
        try:
            return TypeAdapter(t).validate_python(v)
        except PydanticValidationError as ex:
            raise BadRequestException(extra=ex.errors(include_context=False)) from ex

    def _validate_json(self, t: type[T], v: str) -> T:
        try:
            return TypeAdapter(Json[t]).validate_strings(v)
        except PydanticValidationError as ex:
            raise BadRequestException(extra=ex.errors(include_context=False)) from ex

    @handlers.get(
        summary="List playlists",
        description="List playlists that match the request.",
    )
    async def list(
        self,
        service: Service,
        limit: Annotated[
            m.ListRequestLimit,
            Parameter(description="Maximum number of playlists to return.", default=10),
        ] = 10,
        offset: Annotated[
            m.ListRequestOffset,
            Parameter(description="Number of playlists to skip."),
        ] = None,
        where: Annotated[
            str | None,
            Parameter(description="Filter to apply to playlists."),
        ] = None,
        include: Annotated[
            str | None,
            Parameter(description="Relations to include with playlists."),
        ] = None,
        order: Annotated[
            str | None,
            Parameter(description="Order to apply to playlists."),
        ] = None,
    ) -> Response[m.ListResponseResults]:
        where = self._validate_json(m.ListRequestWhere, where) if where else None
        include = (
            self._validate_json(m.ListRequestInclude, include) if include else None
        )
        order = self._validate_json(m.ListRequestOrder, order) if order else None

        try:
            response = await service.list(
                m.ListRequest(
                    limit=limit,
                    offset=offset,
                    where=where,
                    include=include,
                    order=order,
                )
            )
        except e.ValidationError as ex:
            raise BadRequestException(extra=ex.message) from ex

        results = response.results

        return Response(results)

    @handlers.get(
        "/{id:uuid}",
        summary="Get playlist",
        description="Get playlist by ID.",
    )
    async def get(
        self,
        service: Service,
        id: m.GetRequestId,
        include: Annotated[
            str | None,
            Parameter(description="Relations to include with playlist."),
        ] = None,
    ) -> Response[m.GetResponsePlaylist]:
        include = self._validate_json(m.GetRequestInclude, include) if include else None

        try:
            response = await service.get(
                m.GetRequest(
                    id=id,
                    include=include,
                )
            )
        except e.ValidationError as ex:
            raise BadRequestException(extra=ex.message) from ex
        except e.PlaylistNotFoundError as ex:
            raise NotFoundException(extra=ex.message) from ex

        playlist = response.playlist

        return Response(playlist)

    @handlers.post(
        summary="Create playlist",
        description="Create playlist.",
    )
    async def create(
        self,
        service: Service,
        data: m.CreateRequestData,
        include: Annotated[
            str | None,
            Parameter(description="Relations to include with playlist."),
        ] = None,
    ) -> Response[m.CreateResponsePlaylist]:
        data = self._validate_pydantic(m.CreateRequestData, data)
        include = (
            self._validate_json(m.CreateRequestInclude, include) if include else None
        )

        try:
            response = await service.create(
                m.CreateRequest(
                    data=data,
                    include=include,
                )
            )
        except e.ValidationError as ex:
            raise BadRequestException(extra=ex.message) from ex

        playlist = response.playlist

        return Response(playlist)

    @handlers.patch(
        "/{id:uuid}",
        summary="Update playlist",
        description="Update playlist by ID.",
    )
    async def update(
        self,
        service: Service,
        id: m.UpdateRequestId,
        data: m.UpdateRequestData,
        include: Annotated[
            str | None,
            Parameter(description="Relations to include with playlist."),
        ] = None,
    ) -> Response[m.UpdateResponsePlaylist]:
        data = self._validate_pydantic(m.UpdateRequestData, data)
        include = (
            self._validate_json(m.UpdateRequestInclude, include) if include else None
        )

        try:
            response = await service.update(
                m.UpdateRequest(
                    data=data,
                    id=id,
                    include=include,
                )
            )
        except e.ValidationError as ex:
            raise BadRequestException(extra=ex.message) from ex
        except e.PlaylistNotFoundError as ex:
            raise NotFoundException(extra=ex.message) from ex

        playlist = response.playlist

        return Response(playlist)

    @handlers.delete(
        "/{id:uuid}",
        summary="Delete playlist",
        description="Delete playlist by ID.",
    )
    async def delete(
        self,
        service: Service,
        id: m.DeleteRequestId,
    ) -> Response[None]:
        try:
            await service.delete(
                m.DeleteRequest(
                    id=id,
                )
            )
        except e.ValidationError as ex:
            raise BadRequestException(extra=ex.message) from ex
        except e.PlaylistNotFoundError as ex:
            raise NotFoundException(extra=ex.message) from ex

        return Response(None)
