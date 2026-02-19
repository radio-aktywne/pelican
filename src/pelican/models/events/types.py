from typing import Annotated

from pydantic import Field

from pelican.models.events import bindings, media, playlists, test

type Event = Annotated[
    test.TestEvent
    | bindings.BindingCreatedEvent
    | bindings.BindingUpdatedEvent
    | bindings.BindingDeletedEvent
    | media.MediaCreatedEvent
    | media.MediaUpdatedEvent
    | media.MediaDeletedEvent
    | playlists.PlaylistCreatedEvent
    | playlists.PlaylistUpdatedEvent
    | playlists.PlaylistDeletedEvent,
    Field(discriminator="type"),
]
