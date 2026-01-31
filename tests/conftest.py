import pytest
import pytest_asyncio
from py_gamma_sdk import AsyncGammaClient

@pytest_asyncio.fixture
async def client():
    async with AsyncGammaClient() as client:
        yield client
