from typing import Annotated

from pydantic import Field, RootModel

from emitunes.models.events import binding as be
from emitunes.models.events import media as me
from emitunes.models.events import playlist as pe

Event = Annotated[
    be.BindingCreatedEvent
    | be.BindingUpdatedEvent
    | be.BindingDeletedEvent
    | me.MediaCreatedEvent
    | me.MediaUpdatedEvent
    | me.MediaDeletedEvent
    | pe.PlaylistCreatedEvent
    | pe.PlaylistUpdatedEvent
    | pe.PlaylistDeletedEvent,
    Field(..., discriminator="type"),
]
ParsableEvent = RootModel[Event]
