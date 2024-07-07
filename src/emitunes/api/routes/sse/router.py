from litestar import Router

from emitunes.api.routes.sse.controller import Controller

router = Router(
    path="/sse",
    route_handlers=[
        Controller,
    ],
)
