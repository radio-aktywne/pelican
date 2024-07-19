from collections.abc import Generator
from contextlib import contextmanager

from emitunes.api.routes.bindings import errors as e
from emitunes.api.routes.bindings import models as m
from emitunes.bindings import errors as pe
from emitunes.bindings import models as pm
from emitunes.bindings.service import BindingsService


class Service:
    """Service for the bindings endpoint."""

    def __init__(self, bindings: BindingsService) -> None:
        self._bindings = bindings

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
        """List bindings."""

        limit = request.limit
        offset = request.offset
        where = request.where
        include = request.include
        order = request.order

        with self._handle_errors():
            response = await self._bindings.count(
                pm.CountRequest(
                    where=where,
                )
            )

        count = response.count

        with self._handle_errors():
            response = await self._bindings.list(
                pm.ListRequest(
                    limit=limit,
                    offset=offset,
                    where=where,
                    include=include,
                    order=order,
                )
            )

        bindings = response.bindings

        results = m.ListResponseResults(
            count=count,
            limit=limit,
            offset=offset,
            bindings=bindings,
        )
        return m.ListResponse(
            results=results,
        )

    async def get(self, request: m.GetRequest) -> m.GetResponse:
        """Get binding."""

        id = request.id
        include = request.include

        with self._handle_errors():
            response = await self._bindings.get(
                pm.GetRequest(
                    where={
                        "id": str(id),
                    },
                    include=include,
                )
            )

        binding = response.binding

        if binding is None:
            raise e.BindingNotFoundError(id)

        return m.GetResponse(
            binding=binding,
        )

    async def create(self, request: m.CreateRequest) -> m.CreateResponse:
        """Create binding."""

        data = request.data
        include = request.include

        with self._handle_errors():
            response = await self._bindings.create(
                pm.CreateRequest(
                    data=data,
                    include=include,
                )
            )

        binding = response.binding

        return m.CreateResponse(
            binding=binding,
        )

    async def update(self, request: m.UpdateRequest) -> m.UpdateResponse:
        """Update binding."""

        data = request.data
        id = request.id
        include = request.include

        with self._handle_errors():
            response = await self._bindings.update(
                pm.UpdateRequest(
                    data=data,
                    where={
                        "id": str(id),
                    },
                    include=include,
                )
            )

        binding = response.binding

        if binding is None:
            raise e.BindingNotFoundError(id)

        return m.UpdateResponse(
            binding=binding,
        )

    async def delete(self, request: m.DeleteRequest) -> m.DeleteResponse:
        """Delete binding."""

        id = request.id

        with self._handle_errors():
            response = await self._bindings.delete(
                pm.DeleteRequest(
                    where={
                        "id": str(id),
                    },
                )
            )

        binding = response.binding

        if binding is None:
            raise e.BindingNotFoundError(id)

        return m.DeleteResponse()
