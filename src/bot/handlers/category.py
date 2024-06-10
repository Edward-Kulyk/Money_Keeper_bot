from aiogram import F, Router, types
from src.bot.keyboards.category import category_keyboard
from src.bot.keyboards.settings import settings_keyboard

category_router = Router()


@category_router.message(F.text.lower() == "category settings")
async def category_menu(message: types.Message) -> None:
    await message.answer("Category Menu", reply_markup=category_keyboard)


@category_router.message(F.text.lower() == "add new category")
async def add_category(message: types.Message) -> None:
    await message.answer("Please enter the name of the category you want to add:")


@category_router.message(F.text.lower() == "edit existing category")
async def edit_category(message: types.Message) -> None:
    await message.answer("Please enter the name of the category you want to edit:")


@category_router.message(F.text.lower() == "delete category")
async def delete_category(message: types.Message) -> None:
    await message.answer("Please enter the name of the category you want to delete:")


@category_router.message(F.text.lower() == "back to settings")
async def back_to_settings(message: types.Message) -> None:
    await message.answer("Settings Menu", reply_markup=settings_keyboard)
