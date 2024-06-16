from typing import List, Sequence

from sqlalchemy import delete, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src.database.models import Category, User


async def get_all_categories_by_tg_user_id(session: AsyncSession, tg_user_id: int) -> Sequence[Category] | None:
    return (await session.execute(select(Category).join(User).where(User.tg_user_id == tg_user_id))).scalars().all()


async def add_new_category(session: AsyncSession, category: Category):
    session.add(category)


async def check_if_user_have_category(session: AsyncSession, category: str, user_id: int) -> bool:
    return (
        await session.execute(select(Category).where(Category.name == category, Category.owner_id == user_id))
    ).scalars().first() is not None


async def update_category_name(session: AsyncSession, category_id: int, category_new_name: str) -> None:
    await session.execute(update(Category).where(Category.id == category_id).values(name=category_new_name))


async def delete_category(session: AsyncSession, category_id: int):
    await session.execute(delete(Category).where(Category.id == category_id))


async def get_category_name_list(session: AsyncSession, tg_user_id: int) -> List[Category]:
    result = await session.execute(select(Category).join(User).where(User.tg_user_id == tg_user_id))
    categories = result.scalars().all()
    return categories if categories is not None else []


async def get_category_by_name_owner(session: AsyncSession, category_name: str, owner_id: int) -> Category:
    return (
        (await session.execute(select(Category).where(Category.name == category_name, Category.owner_id == owner_id)))
        .scalars()
        .first()
    )
