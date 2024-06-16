from aiogram import F, Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, Message

from src.bot.keyboards.sorting import get_category_suggest_category_keyboard
from src.bot.state import BotPaymentsSorting
from src.repository.category import get_all_categories_by_tg_user_id
from src.services.category import get_category_list_by_tg_id, get_category_object
from src.services.operation import get_suggestion_for_unsorted_payment, get_unsorted_payment_by_tg_id, \
    set_match_shop_category, set_operation_category
from src.services.user import get_user_by_tg_id

sorting_router = Router()


@sorting_router.message(F.text.lower() == "sort payments")
async def sorting_menu(message: Message, state: FSMContext) -> None:
    unsorted_payment = await get_unsorted_payment_by_tg_id(message.from_user.id)

    if unsorted_payment and message:

        categories = await get_category_list_by_tg_id(message.from_user.id)

        suggested_category = await get_suggestion_for_unsorted_payment(unsorted_payment.shop, categories)

        category = await get_category_object(suggested_category, (await get_user_by_tg_id(message.from_user.id)).id)

        await message.answer(
            f"Shop: {unsorted_payment.shop}\n"
            f"Amount: {unsorted_payment.amount / 100} {unsorted_payment.currency}\n"
            f"\nSuggested category: {suggested_category}\n"
            "Do you accept the suggested category?",
            reply_markup=get_category_suggest_category_keyboard(),
        )
        await state.set_state(BotPaymentsSorting.category_suggestion)
        await state.update_data(category_id=category.id, unsorted_payment_id=unsorted_payment.id,
                                shop=unsorted_payment.shop)
    else:
        await message.answer("No unsorted payments found.")


@sorting_router.message(F.text.lower() == "confirm", StateFilter(BotPaymentsSorting.category_suggestion))
async def accept_suggested_category(message: Message, state: FSMContext):
    print("nahij")
    if message:
        user = await get_user_by_tg_id(message.from_user.id)
        user_data = await state.get_data()

        if user.payment_mode == "remember":
            counter = await set_match_shop_category(user_data["shop"], user.id, user_data["category_id"])
            await message.answer(f"{counter} operations was moved")
        else:
            await set_operation_category(user_data["unsorted_payment_id"], user_data["category_id"])
            await message.answer(f"Operation was moved")

        await state.clear()
        await sorting_menu(message, state)


@sorting_router.callback_query(F.data.startswith("reject_"))
async def reject_suggested_category(callback_query: CallbackQuery, state: FSMContext):
    payment_id = int(callback_query.data.split("_")[1])
    user_id = callback_query.from_user.id

    categories = await get_all_categories_by_tg_user_id(user_id)
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=category.name, callback_data=f"category_{payment_id}_{category.id}")]
            for category in categories
        ]
    )
    await callback_query.message.answer("Please choose a category for the payment:", reply_markup=keyboard)
    await callback_query.answer()


@sorting_router.callback_query(F.data.startswith("category_"))
async def handle_category_selection(callback_query: CallbackQuery, state: FSMContext):
    data = callback_query.data.split("_")
    payment_id = int(data[1])
    category_id = int(data[2])

    # Add logic to update the payment with the chosen category
    # await update_payment_category(payment_id, category_id)

    await callback_query.message.answer("Payment sorted successfully!")
    await callback_query.answer()
