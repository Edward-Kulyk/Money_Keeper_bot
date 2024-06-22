from datetime import date
from typing import Any, Sequence

from sqlalchemy import Row, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import Category, Operation


async def get_sum_by_category(
    session: AsyncSession, user_id: int, start_date: date, end_date: date
) -> Sequence[Row[Any]]:
    result = await session.execute(
        select(Category.name, func.sum(Operation.amount).label("total_amount"))
        .join(Operation, Operation.category_id == Category.id)
        .where(Operation.time >= start_date, Operation.time <= end_date, Operation.owner_id == user_id)
        .group_by(Category.name)
    )
    return result.all()
