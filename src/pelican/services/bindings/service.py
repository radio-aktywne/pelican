from collections.abc import Generator, Sequence
from contextlib import contextmanager
from typing import cast

from fractional_indexing import FIError, validate_order_key
from litestar.channels import ChannelsPlugin

from pelican.models.events import binding as ev
from pelican.models.events.event import Event
from pelican.services.bindings import errors as e
from pelican.services.bindings import models as m
from pelican.services.graphite import errors as ge
from pelican.services.graphite import types as gt
from pelican.services.graphite.service import GraphiteService


class BindingsService:
    """Service to manage bindings."""

    def __init__(self, graphite: GraphiteService, channels: ChannelsPlugin) -> None:
        self._graphite = graphite
        self._channels = channels

    def _emit_event(self, event: Event) -> None:
        data = event.model_dump_json(round_trip=True)
        self._channels.publish(data, "events")

    def _emit_binding_created_event(self, binding: m.Binding) -> None:
        self._emit_event(
            ev.BindingCreatedEvent(
                data=ev.BindingCreatedEventData(binding=ev.Binding.map(binding))
            )
        )

    def _emit_binding_updated_event(self, binding: m.Binding) -> None:
        self._emit_event(
            ev.BindingUpdatedEvent(
                data=ev.BindingUpdatedEventData(binding=ev.Binding.map(binding))
            )
        )

    def _emit_binding_deleted_event(self, binding: m.Binding) -> None:
        self._emit_event(
            ev.BindingDeletedEvent(
                data=ev.BindingDeletedEventData(binding=ev.Binding.map(binding))
            )
        )

    @contextmanager
    def _handle_errors(self) -> Generator[None]:
        try:
            yield
        except ge.DataError as ex:
            raise e.ValidationError from ex
        except ge.ServiceError as ex:
            raise e.GraphiteError from ex

    def _validate_rank(self, rank: str) -> None:
        try:
            validate_order_key(rank)
        except FIError as ex:
            raise e.InvalidRankError(rank) from ex

    async def count(self, request: m.CountRequest) -> m.CountResponse:
        """Count bindings."""
        with self._handle_errors():
            count = await self._graphite.binding.count(where=request.where)

        return m.CountResponse(count=count)

    async def list(self, request: m.ListRequest) -> m.ListResponse:
        """List all bindings."""
        with self._handle_errors():
            bindings = await self._graphite.binding.find_many(
                take=request.limit,
                skip=request.offset,
                where=request.where,
                include=request.include,
                order=list(request.order)
                if isinstance(request.order, Sequence)
                else request.order,
            )

        return m.ListResponse(bindings=bindings)

    async def get(self, request: m.GetRequest) -> m.GetResponse:
        """Get binding."""
        with self._handle_errors():
            binding = await self._graphite.binding.find_unique(
                where=request.where, include=request.include
            )

        return m.GetResponse(binding=binding)

    async def create(self, request: m.CreateRequest) -> m.CreateResponse:
        """Create binding."""
        self._validate_rank(request.data["rank"])

        with self._handle_errors():
            binding = await self._graphite.binding.create(
                data=cast("gt.BindingCreateInput", request.data),
                include=request.include,
            )

        self._emit_binding_created_event(binding)

        return m.CreateResponse(binding=binding)

    async def update(self, request: m.UpdateRequest) -> m.UpdateResponse:
        """Update binding."""
        if "rank" in request.data:
            self._validate_rank(request.data["rank"])

        with self._handle_errors():
            binding = await self._graphite.binding.update(
                data=cast("gt.BindingUpdateInput", request.data),
                where=request.where,
                include=request.include,
            )

        if binding is None:
            return m.UpdateResponse(binding=None)

        self._emit_binding_updated_event(binding)

        return m.UpdateResponse(binding=binding)

    async def delete(self, request: m.DeleteRequest) -> m.DeleteResponse:
        """Delete binding."""
        with self._handle_errors():
            binding = await self._graphite.binding.delete(
                where=request.where, include=request.include
            )

        if binding is None:
            return m.DeleteResponse(binding=None)

        self._emit_binding_deleted_event(binding)

        return m.DeleteResponse(binding=binding)
