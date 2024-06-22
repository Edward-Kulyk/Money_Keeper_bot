from .database import Base, engine, get_session

__all__ = ["Base", "engine", "get_session"]


async def init_db() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
