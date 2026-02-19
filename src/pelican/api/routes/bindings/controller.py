from collections.abc import Mapping
from typing import Annotated

from litestar import Controller as BaseController
from litestar import handlers
from litestar.channels import ChannelsPlugin
from litestar.di import Provide
from litestar.params import Body, Parameter
from litestar.response import Response

from pelican.api.exceptions import BadRequestException, NotFoundException
from pelican.api.routes.bindings import errors as e
from pelican.api.routes.bindings import models as m
from pelican.api.routes.bindings.service import Service
from pelican.models.base import Jsonable, Serializable
from pelican.services.bindings.service import BindingsService
from pelican.state import State


class DependenciesBuilder:
    """Builder for the dependencies of the controller."""

    async def _build_service(self, state: State, channels: ChannelsPlugin) -> Service:
        return Service(
            bindings=BindingsService(graphite=state.graphite, channels=channels)
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
        raises=[BadRequestException],
    )
    async def list(  # noqa: PLR0913
        self,
        service: Service,
        limit: Annotated[
            Jsonable[m.ListRequestLimit] | None,
            Parameter(
                description="Maximum number of bindings to return. Default is 10.",
            ),
        ] = None,
        offset: Annotated[
            Jsonable[m.ListRequestOffset] | None,
            Parameter(
                description="Number of bindings to skip.",
            ),
        ] = None,
        where: Annotated[
            Jsonable[m.ListRequestWhere] | None,
            Parameter(
                description="Filter to apply to find bindings.",
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
        """List bindings that match the request."""
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
        summary="Get binding",
        raises=[BadRequestException, NotFoundException],
    )
    async def get(
        self,
        service: Service,
        id: Annotated[  # noqa: A002
            Serializable[m.GetRequestId],
            Parameter(
                description="Identifier of the binding to get.",
            ),
        ],
        include: Annotated[
            Jsonable[m.GetRequestInclude] | None,
            Parameter(
                description="Relations to include in the response.",
            ),
        ] = None,
    ) -> Response[Serializable[m.GetResponseBinding]]:
        """Get a binding by ID."""
        request = m.GetRequest(id=id.root, include=include.root if include else None)

        try:
            response = await service.get(request)
        except e.ValidationError as ex:
            raise BadRequestException from ex
        except e.BindingNotFoundError as ex:
            raise NotFoundException from ex

        return Response(Serializable(response.binding))

    @handlers.post(
        summary="Create binding",
        raises=[BadRequestException],
    )
    async def create(
        self,
        service: Service,
        data: Annotated[
            Serializable[m.CreateRequestData],
            Body(
                description="Data to create a binding.",
            ),
        ],
        include: Annotated[
            Jsonable[m.CreateRequestInclude] | None,
            Parameter(
                description="Relations to include in the response.",
            ),
        ] = None,
    ) -> Response[Serializable[m.CreateResponseBinding]]:
        """Create a new binding."""
        request = m.CreateRequest(
            data=data.root, include=include.root if include else None
        )

        try:
            response = await service.create(request)
        except e.ValidationError as ex:
            raise BadRequestException from ex

        return Response(Serializable(response.binding))

    @handlers.patch(
        "/{id:str}",
        summary="Update binding",
        raises=[BadRequestException, NotFoundException],
    )
    async def update(
        self,
        service: Service,
        id: Annotated[  # noqa: A002
            Serializable[m.UpdateRequestId],
            Parameter(
                description="Identifier of the binding to update.",
            ),
        ],
        data: Annotated[
            Serializable[m.UpdateRequestData],
            Body(
                description="Data to update a binding.",
            ),
        ],
        include: Annotated[
            Jsonable[m.UpdateRequestInclude] | None,
            Parameter(
                description="Relations to include in the response.",
            ),
        ] = None,
    ) -> Response[Serializable[m.UpdateResponseBinding]]:
        """Update a binding by ID."""
        request = m.UpdateRequest(
            data=data.root, id=id.root, include=include.root if include else None
        )

        try:
            response = await service.update(request)
        except e.ValidationError as ex:
            raise BadRequestException from ex
        except e.BindingNotFoundError as ex:
            raise NotFoundException from ex

        return Response(Serializable(response.binding))

    @handlers.delete(
        "/{id:str}",
        summary="Delete binding",
        raises=[BadRequestException, NotFoundException],
    )
    async def delete(
        self,
        service: Service,
        id: Annotated[  # noqa: A002
            Serializable[m.DeleteRequestId],
            Parameter(
                description="Identifier of the binding to delete.",
            ),
        ],
    ) -> None:
        """Delete a binding by ID."""
        request = m.DeleteRequest(id=id.root)

        try:
            await service.delete(request)
        except e.ValidationError as ex:
            raise BadRequestException from ex
        except e.BindingNotFoundError as ex:
            raise NotFoundException from ex
