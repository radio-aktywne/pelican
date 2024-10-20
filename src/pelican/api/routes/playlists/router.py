from litestar import Router

from pelican.api.routes.playlists.controller import Controller

router = Router(
    path="/playlists",
    route_handlers=[
        Controller,
    ],
)
