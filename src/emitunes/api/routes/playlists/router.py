from litestar import Router

from emitunes.api.routes.playlists.controller import Controller

router = Router(
    path="/playlists",
    route_handlers=[
        Controller,
    ],
)
