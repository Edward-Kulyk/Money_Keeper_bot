from datetime import date, timedelta

from aiogram import F, Router, types

from src.bot.keyboards.main_menu import get_main_menu_keyboard
from src.bot.keyboards.statistics import statistics_keyboard
from src.services.statistic import get_statistic_by_category_month
from src.services.user import get_user_by_tg_id

statistics_router = Router()


@statistics_router.message(F.text.lower() == "statistics")
async def statistics_menu(message: types.Message) -> None:
    if message.from_user is None:
        return
    await message.answer("Statistics Menu", reply_markup=statistics_keyboard)


@statistics_router.message(F.text.lower() == "statistics this month")
async def this_month_stats(message: types.Message) -> None:
    today = date.today()
    start_date = today.replace(day=1)
    next_month = today.replace(day=28) + timedelta(days=4)  # this will never fail
    end_date = next_month - timedelta(days=next_month.day)
    if message.from_user is None:
        return
    user = await get_user_by_tg_id(message.from_user.id)
    if user is None:
        await message.answer("User not found.")
        return

    category_sums = await get_statistic_by_category_month(user.id, start_date, end_date)
    if isinstance(category_sums, str):
        await message.answer(category_sums)
    else:
        formatted_results = [f"{row.name}:{row.total_amount / 100}" for row in category_sums]
        await message.answer("\n".join(formatted_results))


@statistics_router.message(F.text.lower() == "statistics previous month")
async def previous_month_stats(message: types.Message) -> None:
    today = date.today()
    first_day_of_current_month = today.replace(day=1)
    end_date = first_day_of_current_month - timedelta(days=1)
    start_date = end_date.replace(day=1)
    if message.from_user is None:
        return
    user = await get_user_by_tg_id(message.from_user.id)
    if user is None:
        await message.answer("User not found.")
        return

    category_sums = await get_statistic_by_category_month(user.id, start_date, end_date)
    if isinstance(category_sums, str):
        await message.answer(category_sums)
    else:
        formatted_results = [f"{row.name}:{row.total_amount / 100}" for row in category_sums]
        await message.answer("\n".join(formatted_results))


@statistics_router.message(F.text.lower() == "custom statistics")
async def custom_stats(message: types.Message) -> None:
    if message.from_user is None:
        return
    await message.answer("Not ready", reply_markup=await get_main_menu_keyboard(message.from_user.id))


@statistics_router.message(F.text.lower() == "back to main menu")
async def back_to_main_menu(message: types.Message) -> None:
    if message.from_user is None:
        return
    await message.answer("Main Menu", reply_markup=await get_main_menu_keyboard(message.from_user.id))
