from aiogram import types

kb_category = [[types.KeyboardButton(text="Add category")],
    [
        types.KeyboardButton(text="Edit category"),
        types.KeyboardButton(text="Delete category"),
    ],
    [types.KeyboardButton(text="Back to settings")],
]

category_keyboard = types.ReplyKeyboardMarkup(
    keyboard=kb_category, resize_keyboard=True, input_field_placeholder="Select command"
)
