from aiogram import types

kb_cancel = [[types.KeyboardButton(text="Cancel")]]

cancel_keyboard = types.ReplyKeyboardMarkup(
    keyboard=kb_cancel,
    resize_keyboard=True,
)
