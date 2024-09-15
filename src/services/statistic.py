from datetime import date
from typing import Any, Sequence

from sqlalchemy import Row

from src.database.database import get_session
from src.repository.statistic import get_sum_by_category
from src.repository.user import get_user_by_tg_user_id


async def get_statistic_by_category_month(
    tg_user_id: int, start_date: date, end_date: date
) -> Sequence[Row[Any]] | str:
    async with get_session() as session:
        user_id = await get_user_by_tg_user_id(session, tg_user_id)
        if not user_id:
            return "Nothing here"
        return await get_sum_by_category(session, user_id.id, start_date, end_date)
