from collections.abc import AsyncGenerator

import pytest
import pytest_asyncio
from httpx import AsyncClient
from litestar import Litestar
from litestar.testing import AsyncTestClient
from prisma import Prisma

from emitunes.api.app import AppBuilder
from emitunes.config.builder import ConfigBuilder
from emitunes.config.models import Config
from tests.utils.containers import AsyncDockerContainer
from tests.utils.waiting.conditions import CallableCondition
from tests.utils.waiting.strategies import TimeoutStrategy
from tests.utils.waiting.waiter import Waiter


@pytest.fixture(scope="session")
def config() -> Config:
    """Loaded configuration."""

    return ConfigBuilder().build()


@pytest.fixture(scope="session")
def app(config: Config) -> Litestar:
    """Reusable application."""

    return AppBuilder(config).build()


@pytest_asyncio.fixture(scope="session")
async def datatunes() -> AsyncGenerator[AsyncDockerContainer, None]:
    """Datatunes container."""

    async def _check() -> None:
        async with Prisma(
            datasource={"url": "postgres://user:password@localhost:41000/database"}
        ):
            return

    container = AsyncDockerContainer(
        "ghcr.io/radio-aktywne/databases/datatunes:latest",
        network="host",
        privileged=True,
    )

    waiter = Waiter(
        condition=CallableCondition(_check),
        strategy=TimeoutStrategy(30),
    )

    async with container as container:
        await waiter.wait()
        yield container


@pytest_asyncio.fixture(scope="session")
async def mediatunes() -> AsyncGenerator[AsyncDockerContainer, None]:
    """Mediatunes container."""

    async def _check() -> None:
        async with AsyncClient(base_url="http://localhost:40000") as client:
            response = await client.get("/minio/health/ready")
            response.raise_for_status()

    container = AsyncDockerContainer(
        "ghcr.io/radio-aktywne/databases/mediatunes:latest",
        network="host",
    )

    waiter = Waiter(
        condition=CallableCondition(_check),
        strategy=TimeoutStrategy(30),
    )

    async with container as container:
        await waiter.wait()
        yield container


@pytest_asyncio.fixture(scope="session")
async def client(
    app: Litestar, datatunes: AsyncDockerContainer, mediatunes: AsyncDockerContainer
) -> AsyncGenerator[AsyncTestClient, None]:
    """Reusable test client."""

    async with AsyncTestClient(app=app) as client:
        yield client
