import pytest_asyncio
from httpx import ASGITransport, AsyncClient

from src.entrypoints.cli import app

# @containers.override(Container)
# class OverridingContainer(containers.DeclarativeContainer):

#     model_consumer = providers.Resource(MagicMock)


@pytest_asyncio.fixture
async def client():
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as client:
        yield client
