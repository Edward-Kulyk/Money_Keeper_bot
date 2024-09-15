from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import User


async def add_user(session: AsyncSession, user: User) -> None:
    session.add(user)


async def get_user_by_tg_user_id(session: AsyncSession, tg_user_id: int) -> User | None:
    user_row = (await session.execute(select(User).where(User.tg_user_id == tg_user_id))).one_or_none()
    return user_row[0] if user_row else None


async def get_user_by_token(session: AsyncSession, token: str) -> User | None:
    result = (await session.execute(select(User).where(User.token == token))).one_or_none()
    return result[0] if result else None


async def get_user_payment_mode(session: AsyncSession, tg_user_id: int) -> str | None:
    return (await session.execute(select(User.payment_mode).where(User.tg_user_id == tg_user_id))).scalar()


async def update_payment_mode(session: AsyncSession, tg_user_id: int, payment_mode: str) -> None:
    await session.execute(update(User).where(User.tg_user_id == tg_user_id).values(payment_mode=payment_mode))
