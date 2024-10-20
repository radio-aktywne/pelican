from litestar import Router

from pelican.api.routes.bindings.controller import Controller

router = Router(
    path="/bindings",
    route_handlers=[
        Controller,
    ],
)
