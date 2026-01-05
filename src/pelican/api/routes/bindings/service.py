from collections.abc import Generator
from contextlib import contextmanager

from pelican.api.routes.bindings import errors as e
from pelican.api.routes.bindings import models as m
from pelican.services.bindings import errors as be
from pelican.services.bindings import models as bm
from pelican.services.bindings.service import BindingsService


class Service:
    """Service for the bindings endpoint."""

    def __init__(self, bindings: BindingsService) -> None:
        self._bindings = bindings

    @contextmanager
    def _handle_errors(self) -> Generator[None]:
        try:
            yield
        except be.ValidationError as ex:
            raise e.ValidationError(str(ex)) from ex
        except be.GraphiteError as ex:
            raise e.GraphiteError(str(ex)) from ex
        except be.ServiceError as ex:
            raise e.ServiceError(str(ex)) from ex

    async def list(self, request: m.ListRequest) -> m.ListResponse:
        """List bindings."""
        limit = request.limit
        offset = request.offset
        where = request.where
        include = request.include
        order = request.order

        req = bm.CountRequest(
            where=where,
        )

        with self._handle_errors():
            res = await self._bindings.count(req)

        count = res.count

        req = bm.ListRequest(
            limit=limit,
            offset=offset,
            where=where,
            include=include,
            order=order,
        )

        with self._handle_errors():
            res = await self._bindings.list(req)

        bindings = res.bindings

        bindings = [m.Binding.map(p) for p in bindings]
        results = m.BindingList(
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
        binding_id = request.id
        include = request.include

        req = bm.GetRequest(
            where={
                "id": str(binding_id),
            },
            include=include,
        )

        with self._handle_errors():
            res = await self._bindings.get(req)

        binding = res.binding

        if binding is None:
            raise e.BindingNotFoundError(binding_id)

        binding = m.Binding.map(binding)
        return m.GetResponse(
            binding=binding,
        )

    async def create(self, request: m.CreateRequest) -> m.CreateResponse:
        """Create binding."""
        data = request.data
        include = request.include

        req = bm.CreateRequest(
            data=data,
            include=include,
        )

        with self._handle_errors():
            res = await self._bindings.create(req)

        binding = res.binding

        binding = m.Binding.map(binding)
        return m.CreateResponse(
            binding=binding,
        )

    async def update(self, request: m.UpdateRequest) -> m.UpdateResponse:
        """Update binding."""
        data = request.data
        binding_id = request.id
        include = request.include

        req = bm.UpdateRequest(
            data=data,
            where={
                "id": str(binding_id),
            },
            include=include,
        )

        with self._handle_errors():
            res = await self._bindings.update(req)

        binding = res.binding

        if binding is None:
            raise e.BindingNotFoundError(binding_id)

        binding = m.Binding.map(binding)
        return m.UpdateResponse(
            binding=binding,
        )

    async def delete(self, request: m.DeleteRequest) -> m.DeleteResponse:
        """Delete binding."""
        binding_id = request.id

        req = bm.DeleteRequest(
            where={
                "id": str(binding_id),
            },
            include=None,
        )

        with self._handle_errors():
            res = await self._bindings.delete(req)

        binding = res.binding

        if binding is None:
            raise e.BindingNotFoundError(binding_id)

        return m.DeleteResponse()
