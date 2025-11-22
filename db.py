from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase



class Base(DeclarativeBase):
    pass


DATABASE_URL = "postgresql+asyncpg://postgres:postgres@localhost/blogdb"

engin = create_async_engine(url=DATABASE_URL, echo=True)

Session = async_sessionmaker(
    bind=engin,
    autoflush=False,
    class_=AsyncSession
)

async def get_db():
    async with Session as session:
        try:
            yield session()
        finally:
            await session.close()


async def create_table():
    async with engin.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)