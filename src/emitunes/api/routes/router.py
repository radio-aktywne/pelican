from litestar import Router

from emitunes.api.routes.bindings.router import router as bindings_router
from emitunes.api.routes.media.router import router as media_router
from emitunes.api.routes.ping.router import router as ping_router
from emitunes.api.routes.playlists.router import router as playlists_router
from emitunes.api.routes.sse.router import router as sse_router

router = Router(
    path="/",
    route_handlers=[
        bindings_router,
        media_router,
        ping_router,
        playlists_router,
        sse_router,
    ],
)
