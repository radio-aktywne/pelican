from litestar import Router

from pelican.api.routes.media.controller import Controller

router = Router(
    path="/media",
    route_handlers=[
        Controller,
    ],
)
