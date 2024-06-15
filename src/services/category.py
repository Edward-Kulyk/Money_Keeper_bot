from src.database.database import get_session
from src.database.models import Category
from src.repository.category import check_if_user_have_category, add_new_category, update_category_name, delete_category
from src.repository.user import get_user_by_tg_user_id


async def add_new_category_from_user(tg_user_id: int, category: str) -> str:
    async with get_session() as session:
        user = await get_user_by_tg_user_id(session, tg_user_id)
        if await check_if_user_have_category(session, category, user.id):
            return "You already have this category"

        await add_new_category(session, Category(name=category, owner_id=user.id))
        return "Category successful added"


async def update_category_name_by_id(category_id: int, new_category_name: str) -> None:
    async with get_session() as session:
        await update_category_name(session, category_id, new_category_name)


async def delete_category_by_id(category_id: int) -> None:
    async with get_session() as session:
        await delete_category(session, category_id)

