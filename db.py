from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase,sessionmaker
from sqlalchemy import text


class Base(DeclarativeBase):
    pass

db_name = "blogdb"

DATABASE_URL = "postgresql+asyncpg://ebrahim:ebrahimpsql@localhost/blogdb"

engine = create_async_engine(url=DATABASE_URL, echo=True)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    autoflush=False,
    class_=AsyncSession
)

async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()


async def create_table():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        
