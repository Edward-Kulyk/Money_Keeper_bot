from aiogram import types

from src.services.operation import get_unsorted_payments_count


async def get_main_menu_keyboard(tg_user_id: int) -> types.ReplyKeyboardMarkup:
    kb_main_menu = [
        [types.KeyboardButton(text=f"Sort payments({await get_unsorted_payments_count(tg_user_id)})")],
        [types.KeyboardButton(text="Statistics")],
        [types.KeyboardButton(text="Settings")],
    ]

    return types.ReplyKeyboardMarkup(
        keyboard=kb_main_menu, resize_keyboard=True, input_field_placeholder="Select command"
    )
