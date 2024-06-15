from aiogram import types

kb_settings = [
    [
        types.KeyboardButton(text="Confirm"),
        types.KeyboardButton(text="Cancel"),
    ]
]

confirm_keyboard = types.ReplyKeyboardMarkup(
    keyboard=kb_settings, resize_keyboard=True, input_field_placeholder="Select command"
)
