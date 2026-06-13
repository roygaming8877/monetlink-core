import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.core.database import get_async_db
from app.models.base import Base

# Use an in-memory SQLite database for blazing fast asynchronous testing
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

engine = create_async_engine(TEST_DATABASE_URL, echo=False)
TestingSessionLocal = sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)

async def override_get_async_db():
    async with TestingSessionLocal() as session:
        yield session

# Override the production database dependency with our test database
app.dependency_overrides[get_async_db] = override_get_async_db

@pytest_asyncio.fixture(autouse=True)
async def prepare_database():
    """Creates fresh database tables before every single test."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest_asyncio.fixture
async def async_client():
    """Provides an asynchronous HTTP client to simulate frontend requests."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        yield client
      
