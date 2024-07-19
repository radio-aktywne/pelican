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
from emitunes.api.routes.bindings import errors as e
from emitunes.api.routes.bindings import models as m
from emitunes.api.routes.bindings.service import Service
from emitunes.bindings.service import BindingsService
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
            bindings=BindingsService(
                datatunes=state.datatunes,
                channels=channels,
            )
        )

    def build(self) -> dict[str, Provide]:
        return {
            "service": Provide(self._build_service),
        }


class Controller(BaseController):
    """Controller for the bindings endpoint."""

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
        summary="List bindings",
        description="List bindings that match the request.",
    )
    async def list(
        self,
        service: Service,
        limit: Annotated[
            m.ListRequestLimit,
            Parameter(description="Maximum number of bindings to return.", default=10),
        ] = 10,
        offset: Annotated[
            m.ListRequestOffset,
            Parameter(description="Number of bindings to skip."),
        ] = None,
        where: Annotated[
            str | None,
            Parameter(description="Filter to apply to bindings."),
        ] = None,
        include: Annotated[
            str | None,
            Parameter(description="Relations to include with bindings."),
        ] = None,
        order: Annotated[
            str | None,
            Parameter(description="Order to apply to bindings."),
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
        summary="Get binding",
        description="Get binding by ID.",
    )
    async def get(
        self,
        service: Service,
        id: m.GetRequestId,
        include: Annotated[
            str | None,
            Parameter(description="Relations to include with binding."),
        ] = None,
    ) -> Response[m.GetResponseBinding]:
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
        except e.BindingNotFoundError as ex:
            raise NotFoundException(extra=ex.message) from ex

        binding = response.binding

        return Response(binding)

    @handlers.post(
        summary="Create binding",
        description="Create binding.",
    )
    async def create(
        self,
        service: Service,
        data: m.CreateRequestData,
        include: Annotated[
            str | None,
            Parameter(description="Relations to include with binding."),
        ] = None,
    ) -> Response[m.CreateResponseBinding]:
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

        binding = response.binding

        return Response(binding)

    @handlers.patch(
        "/{id:uuid}",
        summary="Update binding",
        description="Update binding by ID.",
    )
    async def update(
        self,
        service: Service,
        id: m.UpdateRequestId,
        data: m.UpdateRequestData,
        include: Annotated[
            str | None,
            Parameter(description="Relations to include with binding."),
        ] = None,
    ) -> Response[m.UpdateResponseBinding]:
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
        except e.BindingNotFoundError as ex:
            raise NotFoundException(extra=ex.message) from ex

        binding = response.binding

        return Response(binding)

    @handlers.delete(
        "/{id:uuid}",
        summary="Delete binding",
        description="Delete binding by ID.",
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
        except e.BindingNotFoundError as ex:
            raise NotFoundException(extra=ex.message) from ex

        return Response(None)
