from litestar import Router

from emitunes.api.routes.bindings.controller import Controller

router = Router(
    path="/bindings",
    route_handlers=[
        Controller,
    ],
)
