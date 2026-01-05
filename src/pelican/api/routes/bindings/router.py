from litestar import Router

from pelican.api.routes.bindings.controller import Controller

router = Router(
    path="/bindings",
    tags=["Bindings"],
    route_handlers=[
        Controller,
    ],
)
