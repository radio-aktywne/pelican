import logging
import warnings
from contextlib import AbstractAsyncContextManager, asynccontextmanager
from importlib import metadata
from typing import AsyncGenerator, Callable

from litestar import Litestar, Router
from litestar.channels import ChannelsPlugin
from litestar.channels.backends.memory import MemoryChannelsBackend
from litestar.contrib.pydantic import PydanticPlugin
from litestar.openapi import OpenAPIConfig
from litestar.plugins import PluginProtocol
from urllib3.exceptions import InsecureRequestWarning

from emitunes.api.routes.router import router
from emitunes.config.models import Config
from emitunes.datatunes.service import DatatunesService
from emitunes.mediatunes.service import MediatunesService
from emitunes.state import State


class AppBuilder:
    """Builds the app.

    Args:
        config: Config object.
    """

    def __init__(self, config: Config) -> None:
        self._config = config

    def _get_route_handlers(self) -> list[Router]:
        return [router]

    def _build_openapi_config(self) -> OpenAPIConfig:
        return OpenAPIConfig(
            title="emitunes app",
            version=metadata.version("emitunes"),
            description="Emission playlists 💽",
        )

    def _build_channels_plugin(self) -> ChannelsPlugin:
        return ChannelsPlugin(
            backend=MemoryChannelsBackend(),
            channels=["events"],
        )

    def _build_pydantic_plugin(self) -> PydanticPlugin:
        return PydanticPlugin(
            prefer_alias=True,
        )

    def _build_plugins(self) -> list[PluginProtocol]:
        return [
            self._build_channels_plugin(),
            self._build_pydantic_plugin(),
        ]

    def _build_datatunes(self) -> DatatunesService:
        return DatatunesService(datasource={"url": self._config.datatunes.sql.url})

    def _build_mediatunes(self) -> MediatunesService:
        return MediatunesService(config=self._config.mediatunes)

    def _build_initial_state(self) -> State:
        config = self._config
        datatunes = self._build_datatunes()
        mediatunes = self._build_mediatunes()

        return State(
            {
                "config": config,
                "datatunes": datatunes,
                "mediatunes": mediatunes,
            }
        )

    @asynccontextmanager
    async def _suppress_urllib_warnings_lifespan(
        self, app: Litestar
    ) -> AsyncGenerator[None, None]:
        with warnings.catch_warnings(
            action="ignore",
            category=InsecureRequestWarning,
        ):
            yield

    @asynccontextmanager
    async def _suppress_httpx_logging_lifespan(
        self, app: Litestar
    ) -> AsyncGenerator[None, None]:
        logger = logging.getLogger("httpx")
        disabled = logger.disabled
        logger.disabled = True

        try:
            yield
        finally:
            logger.disabled = disabled

    @asynccontextmanager
    async def _datatunes_lifespan(self, app: Litestar) -> AsyncGenerator[None, None]:
        state: State = app.state

        async with state.datatunes:
            yield

    def _build_lifespan(
        self,
    ) -> list[Callable[[Litestar], AbstractAsyncContextManager]]:
        return [
            self._suppress_urllib_warnings_lifespan,
            self._suppress_httpx_logging_lifespan,
            self._datatunes_lifespan,
        ]

    def build(self) -> Litestar:
        return Litestar(
            route_handlers=self._get_route_handlers(),
            openapi_config=self._build_openapi_config(),
            plugins=self._build_plugins(),
            state=self._build_initial_state(),
            lifespan=self._build_lifespan(),
        )
