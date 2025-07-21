from src.entrypoints.cli import app
from httpx import ASGITransport, AsyncClient
import pytest_asyncio

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

