# Standard Library
from typing import AsyncGenerator

# Third‑Party Libraries
from config import settings
from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor
from sqlalchemy import URL
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

url_ojbect = URL.create(
    drivername=settings.DB_DRIVER,  # asyncpg
    username=settings.DB_USER,
    password=settings.DB_PASSWORD,
    host=settings.DB_HOST,
    port=settings.DB_PORT,
    database=settings.DB_DATABASE,
)

async_engine = create_async_engine(
    url_ojbect,
    echo_pool=True,
)

# instrument SQLAlchemy
SQLAlchemyInstrumentor().instrument(engine=async_engine.sync_engine)

AsyncSessionLocal = async_sessionmaker(bind=async_engine, class_=AsyncSession, expire_on_commit=False)


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency that yields an AsyncSession and ensures it closes after use.
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
