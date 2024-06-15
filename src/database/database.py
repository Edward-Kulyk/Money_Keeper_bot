from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, AsyncAttrs, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.exc import IntegrityError, OperationalError, SQLAlchemyError
from contextlib import asynccontextmanager
from typing import AsyncGenerator, Any

# Database URL configuration
DATABASE_URL = "sqlite+aiosqlite:///./test.db"

# Create an asynchronous engine
engine = create_async_engine(DATABASE_URL, echo=True)

# Configure the sessionmaker for async sessions
async_session = async_sessionmaker(
    engine,
    class_=AsyncSession,
    autoflush=False,
    expire_on_commit=False
)


# Define the base class for models
class Base(AsyncAttrs, DeclarativeBase):
    pass


# Create an async context manager for the session
@asynccontextmanager
async def get_session() -> AsyncGenerator[AsyncSession, Any]:
    async with async_session() as session:
        try:
            async with session.begin():
                yield session
            await session.commit()
        except (IntegrityError, OperationalError, SQLAlchemyError, Exception) as e:
            await session.rollback()
            raise e
