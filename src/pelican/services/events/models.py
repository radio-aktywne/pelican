from collections.abc import AsyncIterator

from pelican.models.base import datamodel
from pelican.models.events.event import Event


@datamodel
class SubscribeRequest:
    """Request to subscribe."""


@datamodel
class SubscribeResponse:
    """Response for subscribe."""

    events: AsyncIterator[Event]
    """Stream of events."""
