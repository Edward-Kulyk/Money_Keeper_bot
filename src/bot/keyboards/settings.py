from aiogram import types

kb_settings = [
    [
        types.KeyboardButton(text="Get token"),
        types.KeyboardButton(text="Category settings"),
    ],
    [types.KeyboardButton(text="Back to main menu")],
    [types.KeyboardButton(text=f"Payments mode:")],
]

settings_keyboard = types.ReplyKeyboardMarkup(
    keyboard=kb_settings, resize_keyboard=True, input_field_placeholder="Select command"
)
