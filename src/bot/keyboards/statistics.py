from aiogram import types

kb_statistics = [
    [
        types.KeyboardButton(text="Statistics this month"),
        types.KeyboardButton(text="Statistics previous month"),
        types.KeyboardButton(text="Custom statistics"),
    ],
    [types.KeyboardButton(text="Back to main menu")],
]

statistics_keyboard = types.ReplyKeyboardMarkup(
    keyboard=kb_statistics, resize_keyboard=True, input_field_placeholder="Select period"
)
