from collections.abc import Mapping
from typing import Annotated

from litestar import Controller as BaseController
from litestar import handlers
from litestar.channels import ChannelsPlugin
from litestar.di import Provide
from litestar.openapi import ResponseSpec
from litestar.params import Body, Parameter
from litestar.response import Response
from litestar.status_codes import HTTP_204_NO_CONTENT

from pelican.api.exceptions import BadRequestException, NotFoundException
from pelican.api.routes.bindings import errors as e
from pelican.api.routes.bindings import models as m
from pelican.api.routes.bindings.service import Service
from pelican.api.validator import Validator
from pelican.services.bindings.service import BindingsService
from pelican.state import State


class DependenciesBuilder:
    """Builder for the dependencies of the controller."""

    async def _build_service(
        self,
        state: State,
        channels: ChannelsPlugin,
    ) -> Service:
        return Service(
            bindings=BindingsService(
                graphite=state.graphite,
                channels=channels,
            )
        )

    def build(self) -> Mapping[str, Provide]:
        """Build the dependencies."""
        return {
            "service": Provide(self._build_service),
        }


class Controller(BaseController):
    """Controller for the bindings endpoint."""

    dependencies = DependenciesBuilder().build()

    @handlers.get(
        summary="List bindings",
    )
    async def list(  # noqa: PLR0913
        self,
        service: Service,
        limit: Annotated[
            m.ListRequestLimit,
            Parameter(
                description="Maximum number of bindings to return.",
            ),
        ] = 10,
        offset: Annotated[
            m.ListRequestOffset,
            Parameter(
                description="Number of bindings to skip.",
            ),
        ] = None,
        where: Annotated[
            str | None,
            Parameter(
                description="Filter to apply to find bindings.",
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
        """List bindings that match the request."""
        parsed_where = (
            Validator[m.ListRequestWhere].validate_json(where) if where else None
        )
        parsed_include = (
            Validator[m.ListRequestInclude].validate_json(include) if include else None
        )
        parsed_order = (
            Validator[m.ListRequestOrder].validate_json(order) if order else None
        )

        req = m.ListRequest(
            limit=limit,
            offset=offset,
            where=parsed_where,
            include=parsed_include,
            order=parsed_order,
        )

        try:
            res = await service.list(req)
        except e.ValidationError as ex:
            raise BadRequestException from ex

        results = res.results

        return Response(results)

    @handlers.get(
        "/{id:uuid}",
        summary="Get binding",
    )
    async def get(
        self,
        service: Service,
        id: Annotated[  # noqa: A002
            m.GetRequestId,
            Parameter(
                description="Identifier of the binding to get.",
            ),
        ],
        include: Annotated[
            str | None,
            Parameter(
                description="Relations to include in the response.",
            ),
        ] = None,
    ) -> Response[m.GetResponseBinding]:
        """Get a binding by ID."""
        parsed_include = (
            Validator[m.GetRequestInclude].validate_json(include) if include else None
        )

        req = m.GetRequest(
            id=id,
            include=parsed_include,
        )

        try:
            res = await service.get(req)
        except e.ValidationError as ex:
            raise BadRequestException from ex
        except e.BindingNotFoundError as ex:
            raise NotFoundException from ex

        binding = res.binding

        return Response(binding)

    @handlers.post(
        summary="Create binding",
    )
    async def create(
        self,
        service: Service,
        data: Annotated[
            m.CreateRequestData,
            Body(
                description="Data to create a binding.",
            ),
        ],
        include: Annotated[
            str | None,
            Parameter(
                description="Relations to include in the response.",
            ),
        ] = None,
    ) -> Response[m.CreateResponseBinding]:
        """Create a new binding."""
        parsed_data = Validator[m.CreateRequestData].validate_object(data)
        parsed_include = (
            Validator[m.CreateRequestInclude].validate_json(include)
            if include
            else None
        )

        req = m.CreateRequest(
            data=parsed_data,
            include=parsed_include,
        )

        try:
            res = await service.create(req)
        except e.ValidationError as ex:
            raise BadRequestException from ex

        binding = res.binding

        return Response(binding)

    @handlers.patch(
        "/{id:uuid}",
        summary="Update binding",
    )
    async def update(
        self,
        service: Service,
        id: Annotated[  # noqa: A002
            m.UpdateRequestId,
            Parameter(
                description="Identifier of the binding to update.",
            ),
        ],
        data: Annotated[
            m.UpdateRequestData,
            Body(
                description="Data to update a binding.",
            ),
        ],
        include: Annotated[
            str | None,
            Parameter(
                description="Relations to include in the response.",
            ),
        ] = None,
    ) -> Response[m.UpdateResponseBinding]:
        """Update a binding by ID."""
        parsed_data = Validator[m.UpdateRequestData].validate_object(data)
        parsed_include = (
            Validator[m.UpdateRequestInclude].validate_json(include)
            if include
            else None
        )

        req = m.UpdateRequest(
            data=parsed_data,
            id=id,
            include=parsed_include,
        )

        try:
            res = await service.update(req)
        except e.ValidationError as ex:
            raise BadRequestException from ex
        except e.BindingNotFoundError as ex:
            raise NotFoundException from ex

        binding = res.binding

        return Response(binding)

    @handlers.delete(
        "/{id:uuid}",
        summary="Delete binding",
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
            m.DeleteRequestId,
            Parameter(
                description="Identifier of the binding to delete.",
            ),
        ],
    ) -> Response[None]:
        """Delete a binding by ID."""
        req = m.DeleteRequest(
            id=id,
        )

        try:
            await service.delete(req)
        except e.ValidationError as ex:
            raise BadRequestException from ex
        except e.BindingNotFoundError as ex:
            raise NotFoundException from ex

        return Response(None)
