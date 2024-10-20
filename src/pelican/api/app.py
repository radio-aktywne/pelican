import logging
import warnings
from collections.abc import AsyncGenerator, Callable
from contextlib import AbstractAsyncContextManager, asynccontextmanager
from importlib import metadata

from litestar import Litestar, Router
from litestar.channels import ChannelsPlugin
from litestar.channels.backends.memory import MemoryChannelsBackend
from litestar.contrib.pydantic import PydanticPlugin
from litestar.openapi import OpenAPIConfig
from litestar.plugins import PluginProtocol
from urllib3.exceptions import InsecureRequestWarning

from pelican.api.routes.router import router
from pelican.config.models import Config
from pelican.services.graphite.service import GraphiteService
from pelican.services.minium.service import MiniumService
from pelican.state import State


class AppBuilder:
    """Builds the app.

    Args:
        config: Config object.
    """

    def __init__(self, config: Config) -> None:
        self._config = config

    def _get_route_handlers(self) -> list[Router]:
        return [router]

    def _get_debug(self) -> bool:
        return self._config.debug

    @asynccontextmanager
    async def _suppress_urllib_warnings_lifespan(
        self, app: Litestar
    ) -> AsyncGenerator[None]:
        with warnings.catch_warnings(
            action="ignore",
            category=InsecureRequestWarning,
        ):
            yield

    @asynccontextmanager
    async def _suppress_httpx_logging_lifespan(
        self, app: Litestar
    ) -> AsyncGenerator[None]:
        logger = logging.getLogger("httpx")
        disabled = logger.disabled
        logger.disabled = True

        try:
            yield
        finally:
            logger.disabled = disabled

    @asynccontextmanager
    async def _graphite_lifespan(self, app: Litestar) -> AsyncGenerator[None]:
        state: State = app.state

        async with state.graphite:
            yield

    def _build_lifespan(
        self,
    ) -> list[Callable[[Litestar], AbstractAsyncContextManager]]:
        return [
            self._suppress_urllib_warnings_lifespan,
            self._suppress_httpx_logging_lifespan,
            self._graphite_lifespan,
        ]

    def _build_openapi_config(self) -> OpenAPIConfig:
        return OpenAPIConfig(
            # Title of the service
            title="pelican",
            # Version of the service
            version=metadata.version("pelican"),
            # Description of the service
            summary="Broadcast playlists 💽",
            # Use handler docstrings as operation descriptions
            use_handler_docstrings=True,
            # Endpoint to serve the OpenAPI docs from
            path="/schema",
        )

    def _build_channels_plugin(self) -> ChannelsPlugin:
        return ChannelsPlugin(
            # Store events in memory (good only for single instance services)
            backend=MemoryChannelsBackend(),
            # Channels to handle
            channels=["events"],
            # Don't allow channels outside of the list above
            arbitrary_channels_allowed=False,
        )

    def _build_pydantic_plugin(self) -> PydanticPlugin:
        return PydanticPlugin(
            # Use aliases for serialization
            prefer_alias=True,
            # Allow type coercion
            validate_strict=False,
        )

    def _build_plugins(self) -> list[PluginProtocol]:
        return [
            self._build_channels_plugin(),
            self._build_pydantic_plugin(),
        ]

    def _build_graphite(self) -> GraphiteService:
        return GraphiteService(
            datasource={
                "url": self._config.graphite.sql.url,
            },
        )

    def _build_minium(self) -> MiniumService:
        return MiniumService(
            config=self._config.minium,
        )

    def _build_initial_state(self) -> State:
        config = self._config
        graphite = self._build_graphite()
        minium = self._build_minium()

        return State(
            {
                "config": config,
                "graphite": graphite,
                "minium": minium,
            }
        )

    def build(self) -> Litestar:
        return Litestar(
            route_handlers=self._get_route_handlers(),
            debug=self._get_debug(),
            lifespan=self._build_lifespan(),
            openapi_config=self._build_openapi_config(),
            plugins=self._build_plugins(),
            state=self._build_initial_state(),
        )
