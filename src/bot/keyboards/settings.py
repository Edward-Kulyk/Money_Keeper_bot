from aiogram import types

from src.services.user import get_user_payment_mode_by_tg_id


async def get_setting_menu(tg_user_id: int) -> types.ReplyKeyboardMarkup:
    kb_settings = [
        [
            types.KeyboardButton(text="Get token"),
            types.KeyboardButton(text="Category settings"),
        ],
        [types.KeyboardButton(text=f"Payments mode: {await get_user_payment_mode_by_tg_id(tg_user_id)}")],
        [types.KeyboardButton(text="Back to main menu")],
    ]

    return types.ReplyKeyboardMarkup(
        keyboard=kb_settings, resize_keyboard=True, input_field_placeholder="Select command"
    )
