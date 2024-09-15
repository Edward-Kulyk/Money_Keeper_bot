from typing import Sequence

from sqlalchemy import asc, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import Operation


async def add_unsorted_operation(session: AsyncSession, operation: Operation) -> None:
    session.add(operation)


async def get_unsorted_payment(session: AsyncSession, user_id: int) -> Operation | None:
    operation_row = (
        (
            await session.execute(
                select(Operation)
                .where(Operation.owner_id == user_id, Operation.category_id.is_(None))
                .order_by(asc(Operation.time))
            )
        )
        .scalars()
        .first()
    )
    return operation_row if operation_row else None


async def get_unsorted_operation_by_shop_user_id(
    session: AsyncSession, user_id: int, shop: str
) -> Sequence[Operation] | None:
    query = (
        (
            await session.execute(
                select(Operation).where(
                    Operation.owner_id == user_id, Operation.shop == shop, Operation.category_id.is_(None)
                )
            )
        )
        .scalars()
        .all()
    )
    return query


async def get_unsorted_payment_by_id(session: AsyncSession, operation_id: int) -> Operation | None:
    return (await session.execute(select(Operation).where(Operation.id == operation_id))).scalars().first()


async def get_unsorted_payment_count(session: AsyncSession, owner_id: int) -> int:
    result = await session.execute(
        select(func.count(Operation.id)).where(Operation.owner_id == owner_id, Operation.category_id.is_(None))
    )
    return result.scalar() or 0
