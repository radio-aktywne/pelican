from collections.abc import AsyncGenerator

import pytest
import pytest_asyncio
from httpx import AsyncClient
from litestar import Litestar
from litestar.testing import AsyncTestClient
from prisma import Prisma

from pelican.api.app import AppBuilder
from pelican.config.builder import ConfigBuilder
from pelican.config.models import Config
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


@pytest_asyncio.fixture(loop_scope="session", scope="session")
async def graphite() -> AsyncGenerator[AsyncDockerContainer]:
    """Graphite container."""

    async def _check() -> None:
        async with Prisma(
            datasource={"url": "postgres://user:password@localhost:10220/database"}
        ):
            return

    container = AsyncDockerContainer(
        "ghcr.io/radio-aktywne/databases/graphite:latest",
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


@pytest_asyncio.fixture(loop_scope="session", scope="session")
async def minium() -> AsyncGenerator[AsyncDockerContainer]:
    """Minium container."""

    async def _check() -> None:
        async with AsyncClient(base_url="http://localhost:10210") as client:
            response = await client.get("/minio/health/ready")
            response.raise_for_status()

    container = AsyncDockerContainer(
        "ghcr.io/radio-aktywne/databases/minium:latest",
        network="host",
    )

    waiter = Waiter(
        condition=CallableCondition(_check),
        strategy=TimeoutStrategy(30),
    )

    async with container as container:
        await waiter.wait()
        yield container


@pytest_asyncio.fixture(loop_scope="session", scope="session")
async def client(
    app: Litestar, graphite: AsyncDockerContainer, minium: AsyncDockerContainer
) -> AsyncGenerator[AsyncTestClient]:
    """Reusable test client."""

    async with AsyncTestClient(app=app) as client:
        yield client
