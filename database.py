from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker,AsyncGe
from sqlalchemy.orm import declarative_base
from config import settings


engin = create_async_engine(
    url=settings.DATABASE_URL,
    echo=True,
    future=True,
    pool_size=20,
    max_overflow=0,
)

Session = async_sessionmaker(
    engin,
    expire_on_commit=False,
    class_=AsyncSession,
    autoflush=False,
    autocommit=False,
)

class Base(declarative_base()):
    pass


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with Session() as session:
        try:
            yield session
        finally:
            await session.close()
            

async def init_db():
    async with engin.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def drop_db():
    async with engin.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


