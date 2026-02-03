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
            raise e.ValidationError from ex
        except be.GraphiteError as ex:
            raise e.GraphiteError from ex
        except be.ServiceError as ex:
            raise e.ServiceError from ex

    async def list(self, request: m.ListRequest) -> m.ListResponse:
        """List bindings."""
        count_request = bm.CountRequest(where=request.where)

        with self._handle_errors():
            count_response = await self._bindings.count(count_request)

        list_request = bm.ListRequest(
            limit=request.limit,
            offset=request.offset,
            where=request.where,
            include=request.include,
            order=request.order,
        )

        with self._handle_errors():
            list_response = await self._bindings.list(list_request)

        return m.ListResponse(
            results=m.BindingList(
                count=count_response.count,
                limit=request.limit,
                offset=request.offset,
                bindings=[m.Binding.map(binding) for binding in list_response.bindings],
            )
        )

    async def get(self, request: m.GetRequest) -> m.GetResponse:
        """Get binding."""
        get_request = bm.GetRequest(
            where={"id": str(request.id)}, include=request.include
        )

        with self._handle_errors():
            get_response = await self._bindings.get(get_request)

        if get_response.binding is None:
            raise e.BindingNotFoundError(request.id)

        return m.GetResponse(binding=m.Binding.map(get_response.binding))

    async def create(self, request: m.CreateRequest) -> m.CreateResponse:
        """Create binding."""
        create_request = bm.CreateRequest(data=request.data, include=request.include)

        with self._handle_errors():
            create_response = await self._bindings.create(create_request)

        return m.CreateResponse(binding=m.Binding.map(create_response.binding))

    async def update(self, request: m.UpdateRequest) -> m.UpdateResponse:
        """Update binding."""
        update_request = bm.UpdateRequest(
            data=request.data, where={"id": str(request.id)}, include=request.include
        )

        with self._handle_errors():
            update_response = await self._bindings.update(update_request)

        if update_response.binding is None:
            raise e.BindingNotFoundError(request.id)

        return m.UpdateResponse(binding=m.Binding.map(update_response.binding))

    async def delete(self, request: m.DeleteRequest) -> m.DeleteResponse:
        """Delete binding."""
        delete_request = bm.DeleteRequest(where={"id": str(request.id)}, include=None)

        with self._handle_errors():
            delete_response = await self._bindings.delete(delete_request)

        if delete_response.binding is None:
            raise e.BindingNotFoundError(request.id)

        return m.DeleteResponse()
