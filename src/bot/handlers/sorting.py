from aiogram import F, Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from src.bot.handlers.main_menu import main_menu_cmd
from src.bot.keyboards.category_inline import get_categories_keyboard
from src.bot.keyboards.main_menu import get_main_menu_keyboard
from src.bot.keyboards.sorting import get_category_suggest_category_keyboard
from src.bot.state import BotPaymentsSorting
from src.services.category import get_category_list_by_tg_id, get_category_object
from src.services.operation import get_suggestion_for_unsorted_payment, get_unsorted_payment_by_tg_id, \
    sort_operation
from src.services.user import get_user_by_tg_id

sorting_router = Router()


@sorting_router.message(F.text.lower().startswith("sort payments"))
async def sorting_menu(message: Message, state: FSMContext) -> None:

    local_state = await state.get_state()
    tg_id = (await state.get_data()).get("tg_id") if local_state == BotPaymentsSorting.category_suggestion else message.from_user.id
    unsorted_payment = await get_unsorted_payment_by_tg_id(tg_id)

    if unsorted_payment and message:

        categories = await get_category_list_by_tg_id(tg_id)
        suggested_category = await get_suggestion_for_unsorted_payment(unsorted_payment.shop, categories)
        category = await get_category_object(suggested_category, (await get_user_by_tg_id(tg_id)).id)

        await message.answer(
            f"Shop: {unsorted_payment.shop}\n"
            f"Amount: {unsorted_payment.amount / 100} {unsorted_payment.currency}\n"
            f"\nSuggested category: {suggested_category}\n"
            "Do you accept the suggested category?",
            reply_markup=get_category_suggest_category_keyboard(),
        )

        await state.set_state(BotPaymentsSorting.category_suggestion)
        await state.update_data(category_id=category.id, unsorted_payment_id=unsorted_payment.id,
                                shop=unsorted_payment.shop, tg_id=tg_id)

    else:

        await message.answer("No unsorted payments found.")
        await main_menu_cmd(message)


@sorting_router.message(F.text.lower() == "confirm", StateFilter(BotPaymentsSorting.category_suggestion))
async def accept_suggested_category(message: Message, state: FSMContext):
    if message:
        user = await get_user_by_tg_id(message.from_user.id)
        user_data = await state.get_data()
        await message.answer(await sort_operation(user, user_data))

        await state.clear()
        await sorting_menu(message, state)


@sorting_router.message(F.text.lower() == "pick category", StateFilter(BotPaymentsSorting.category_suggestion))
async def reject_suggested_category(message: Message):
    await message.answer("Please choose a category for the payment:",
                         reply_markup=await get_categories_keyboard(message.from_user.id, "select_category"))


@sorting_router.callback_query(F.data.startswith("select_category_"))
async def handle_category_selection(callback_query: CallbackQuery, state: FSMContext):
    data = callback_query.data.split("_")

    user = await get_user_by_tg_id(callback_query.from_user.id)
    user_data = await state.get_data()
    user_data["category_id"] = int(data[2])

    await state.update_data(tg_id=callback_query.from_user.id)
    await state.set_state(BotPaymentsSorting.category_suggestion)

    await callback_query.answer(await sort_operation(user, user_data))

    await callback_query.message.answer("Payment sorted successfully!")
    await callback_query.message.delete()
    await sorting_menu(callback_query.message, state)


@sorting_router.message(F.text.lower() == "back", StateFilter(BotPaymentsSorting.category_suggestion))
async def back_to_main_menu(message: Message, state: FSMContext):
    await message.answer("Main Menu", reply_markup=await get_main_menu_keyboard(message.from_user.id))
    await state.clear()
