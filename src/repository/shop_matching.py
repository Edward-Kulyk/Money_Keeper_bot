from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import ShopCategory


async def add_shop_matching(session: AsyncSession, match: ShopCategory) -> None:
    session.add(match)


async def get_category_by_shop(session: AsyncSession, shop: str, owner_id) -> int | None:
    return (
        await session.execute(
            select(ShopCategory.category_id).where(ShopCategory.shop_name == shop, ShopCategory.owner_id == owner_id)
        )
    ).scalar_one_or_none()
