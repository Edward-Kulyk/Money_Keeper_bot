from typing import List, Sequence

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from src.database.models import Category, User


async def get_all_categories_by_tg_user_id(session: AsyncSession, tg_user_id: str) -> Sequence[Category] | None:
    result = await session.execute(select(Category).join(User).where(User.tg_user_id == tg_user_id))
    return result.scalars().all()
