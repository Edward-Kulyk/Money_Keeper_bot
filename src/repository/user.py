from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.models import User


async def add_user(session: AsyncSession, user: User) -> None:
    session.add(user)


async def get_user_by_tg_user_id(session: AsyncSession, tg_user_id: str) -> User|None:
    result = await session.execute(select(User).where(User.tg_user_id == tg_user_id))
    return result.scalars().one_or_none()
