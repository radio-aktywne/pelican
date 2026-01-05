from typing import Annotated

from pydantic import Field, RootModel

from pelican.models.events import binding as be
from pelican.models.events import media as me
from pelican.models.events import playlist as pe

type Event = Annotated[
    be.BindingCreatedEvent
    | be.BindingUpdatedEvent
    | be.BindingDeletedEvent
    | me.MediaCreatedEvent
    | me.MediaUpdatedEvent
    | me.MediaDeletedEvent
    | pe.PlaylistCreatedEvent
    | pe.PlaylistUpdatedEvent
    | pe.PlaylistDeletedEvent,
    Field(discriminator="type"),
]
ParsableEvent = RootModel[Event]
