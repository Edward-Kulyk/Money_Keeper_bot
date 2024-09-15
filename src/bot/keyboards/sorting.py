from aiogram import types
from aiogram.types import ReplyKeyboardMarkup


def get_category_suggest_category_keyboard() -> ReplyKeyboardMarkup:
    kb_settings = [
        [
            types.KeyboardButton(text="Confirm"),
            types.KeyboardButton(text="Pick category"),
        ],
        [types.KeyboardButton(text="Back")],
    ]

    return types.ReplyKeyboardMarkup(
        keyboard=kb_settings, resize_keyboard=True, input_field_placeholder="Select command"
    )
