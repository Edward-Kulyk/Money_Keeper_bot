from aiogram import types

kb_main_menu = [[types.KeyboardButton(text="Statistics")], [types.KeyboardButton(text="Settings")]]

main_menu_keyboard = types.ReplyKeyboardMarkup(
    keyboard=kb_main_menu, resize_keyboard=True, input_field_placeholder="Select command"
)
