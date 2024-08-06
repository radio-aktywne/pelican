from collections.abc import Generator
from contextlib import contextmanager

from fractional_indexing import FIError, validate_order_key
from litestar.channels import ChannelsPlugin

from emitunes.models.events import binding as ev
from emitunes.models.events.event import Event
from emitunes.services.bindings import errors as e
from emitunes.services.bindings import models as m
from emitunes.services.datatunes import errors as de
from emitunes.services.datatunes.service import DatatunesService


class BindingsService:
    """Service to manage bindings."""

    def __init__(
        self,
        datatunes: DatatunesService,
        channels: ChannelsPlugin,
    ) -> None:
        self._datatunes = datatunes
        self._channels = channels

    def _emit_event(self, event: Event) -> None:
        data = event.model_dump_json(by_alias=True)
        self._channels.publish(data, "events")

    def _emit_binding_created_event(self, binding: m.Binding) -> None:
        binding = ev.Binding.map(binding)
        data = ev.BindingCreatedEventData(
            binding=binding,
        )
        event = ev.BindingCreatedEvent(
            data=data,
        )
        self._emit_event(event)

    def _emit_binding_updated_event(self, binding: m.Binding) -> None:
        binding = ev.Binding.map(binding)
        data = ev.BindingUpdatedEventData(
            binding=binding,
        )
        event = ev.BindingUpdatedEvent(
            data=data,
        )
        self._emit_event(event)

    def _emit_binding_deleted_event(self, binding: m.Binding) -> None:
        binding = ev.Binding.map(binding)
        data = ev.BindingDeletedEventData(
            binding=binding,
        )
        event = ev.BindingDeletedEvent(
            data=data,
        )
        self._emit_event(event)

    @contextmanager
    def _handle_errors(self) -> Generator[None]:
        try:
            yield
        except de.DataError as ex:
            raise e.ValidationError(str(ex)) from ex
        except de.ServiceError as ex:
            raise e.DatatunesError(str(ex)) from ex

    def _validate_rank(self, rank: str) -> None:
        try:
            validate_order_key(rank)
        except FIError as ex:
            raise e.InvalidRankError(rank) from ex

    async def count(self, request: m.CountRequest) -> m.CountResponse:
        """Count bindings."""

        where = request.where

        with self._handle_errors():
            count = await self._datatunes.binding.count(
                where=where,
            )

        return m.CountResponse(
            count=count,
        )

    async def list(self, request: m.ListRequest) -> m.ListResponse:
        """List all bindings."""

        limit = request.limit
        offset = request.offset
        where = request.where
        include = request.include
        order = request.order

        with self._handle_errors():
            bindings = await self._datatunes.binding.find_many(
                take=limit,
                skip=offset,
                where=where,
                include=include,
                order=order,
            )

        return m.ListResponse(
            bindings=bindings,
        )

    async def get(self, request: m.GetRequest) -> m.GetResponse:
        """Get binding."""

        where = request.where
        include = request.include

        with self._handle_errors():
            binding = await self._datatunes.binding.find_unique(
                where=where,
                include=include,
            )

        return m.GetResponse(
            binding=binding,
        )

    async def create(self, request: m.CreateRequest) -> m.CreateResponse:
        """Create binding."""

        data = request.data
        include = request.include

        self._validate_rank(data["rank"])

        with self._handle_errors():
            binding = await self._datatunes.binding.create(
                data=data,
                include=include,
            )

        self._emit_binding_created_event(binding)

        return m.CreateResponse(
            binding=binding,
        )

    async def update(self, request: m.UpdateRequest) -> m.UpdateResponse:
        """Update binding."""

        data = request.data
        where = request.where
        include = request.include

        if "rank" in data:
            self._validate_rank(data["rank"])

        with self._handle_errors():
            binding = await self._datatunes.binding.update(
                data=data,
                where=where,
                include=include,
            )

        if binding is None:
            return m.UpdateResponse(
                binding=None,
            )

        self._emit_binding_updated_event(binding)

        return m.UpdateResponse(
            binding=binding,
        )

    async def delete(self, request: m.DeleteRequest) -> m.DeleteResponse:
        """Delete binding."""

        where = request.where
        include = request.include

        with self._handle_errors():
            binding = await self._datatunes.binding.delete(
                where=where,
                include=include,
            )

        if binding is None:
            return m.DeleteResponse(
                binding=None,
            )

        self._emit_binding_deleted_event(binding)

        return m.DeleteResponse(
            binding=binding,
        )
