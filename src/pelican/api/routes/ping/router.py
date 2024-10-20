from litestar import Router

from pelican.api.routes.ping.controller import Controller

router = Router(
    path="/ping",
    route_handlers=[
        Controller,
    ],
)
