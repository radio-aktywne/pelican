from litestar import Router

from emitunes.api.routes.ping.controller import Controller

router = Router(
    path="/ping",
    route_handlers=[
        Controller,
    ],
)
