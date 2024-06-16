from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from src.database.database import get_session
from src.repository.category import get_all_categories_by_tg_user_id


async def get_categories_keyboard(tg_user_id: int, callback_handler: str) -> InlineKeyboardMarkup | None:
    async with get_session() as session:
        categories = await get_all_categories_by_tg_user_id(session, tg_user_id)

        if categories is None:
            return None

        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text=category.name, callback_data=f"{callback_handler}_{category.id}")]
                for category in categories
            ]
        )
        return keyboard
