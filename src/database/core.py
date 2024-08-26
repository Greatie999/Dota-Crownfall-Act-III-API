from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker
)

from src.settings import settings

engine = create_async_engine(
    url=settings.DB_URL,
    echo=False,
    pool_size=10,
    max_overflow=5
)
async_session_factory = async_sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False
)


async def get_async_session():
    async with async_session_factory() as session:
        try:
            yield session
        finally:
            await session.close()
