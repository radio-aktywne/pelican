from collections.abc import AsyncIterator

from emitunes.models.base import datamodel


@datamodel
class SubscribeRequest:
    """Request to subscribe."""

    pass


@datamodel
class SubscribeResponse:
    """Response for subscribe."""

    messages: AsyncIterator[str]
    """Stream of messages."""
