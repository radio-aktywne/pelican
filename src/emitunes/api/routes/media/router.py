from litestar import Router

from emitunes.api.routes.media.controller import Controller

router = Router(
    path="/media",
    route_handlers=[
        Controller,
    ],
)
