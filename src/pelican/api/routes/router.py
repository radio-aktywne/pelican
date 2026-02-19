from litestar import Router

from pelican.api.routes.bindings.router import router as bindings
from pelican.api.routes.media.router import router as media
from pelican.api.routes.ping.router import router as ping
from pelican.api.routes.playlists.router import router as playlists
from pelican.api.routes.sse.router import router as sse
from pelican.api.routes.test.router import router as test

router = Router(
    path="/",
    route_handlers=[
        bindings,
        media,
        ping,
        playlists,
        sse,
        test,
    ],
)
