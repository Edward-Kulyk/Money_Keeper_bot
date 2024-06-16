from aiogram import F, Router, types

from src.bot.keyboards.main_menu import main_menu_keyboard
from src.bot.keyboards.statistics import statistics_keyboard

statistics_router = Router()


@statistics_router.message(F.text.lower() == "statistics")
async def statistics_menu(message: types.Message) -> None:
    await message.answer("Statistics Menu", reply_markup=statistics_keyboard)


@statistics_router.message(F.text.lower() == "statistics this month")
async def this_month_stats(message: types.Message) -> None:
    await message.answer("Not ready", reply_markup=main_menu_keyboard)


@statistics_router.message(F.text.lower() == "statistics previous month")
async def previous_month_stats(message: types.Message) -> None:
    await message.answer("Not ready", reply_markup=main_menu_keyboard)


@statistics_router.message(F.text.lower() == "custom statistics")
async def custom_stats(message: types.Message) -> None:
    await message.answer("Not ready", reply_markup=main_menu_keyboard)


@statistics_router.message(F.text.lower() == "back to main menu")
async def back_to_main_menu(message: types.Message) -> None:
    await message.answer("Main Menu", reply_markup=main_menu_keyboard)
