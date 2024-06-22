from aiogram import Router, types
from aiogram.filters import Command

from src.bot.keyboards.main_menu import get_main_menu_keyboard

main_menu_router = Router()


@main_menu_router.message(Command("start"))
async def main_menu(message: types.Message) -> None:
    if message.from_user and message.text:
        await message.answer("Main Menu", reply_markup=await get_main_menu_keyboard(message.from_user.id))


@main_menu_router.message(Command("main"))
async def main_menu_cmd(message: types.Message) -> None:
    if message.from_user and message.text:
        await message.answer("Main Menu", reply_markup=await get_main_menu_keyboard(message.from_user.id))
