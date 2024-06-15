from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.models import User


async def add_user(session: AsyncSession, user: User) -> None:
    session.add(user)


async def get_user_by_tg_user_id(session: AsyncSession, tg_user_id: int) -> User | None:
    return (await session.execute(select(User).where(User.tg_user_id == tg_user_id))).scalars().one_or_none()


async def get_user_payment_mode(session: AsyncSession, tg_user_id: int) -> str | None:
    return (await session.execute(select(User.payment_mode).where(User.tg_user_id == tg_user_id))).scalar()


async def update_payment_mode(session: AsyncSession, tg_user_id: int, payment_mode: str) -> None:
    print(payment_mode)
    await session.execute(update(User).where(User.tg_user_id == tg_user_id).values(payment_mode=payment_mode))
