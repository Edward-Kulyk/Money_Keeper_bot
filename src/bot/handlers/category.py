from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.filters.state import StateFilter

from src.bot.keyboards.cancel_button import cancel_keyboard
from src.bot.keyboards.category import category_keyboard
from src.bot.keyboards.category_inline import get_categories_keyboard
from src.bot.keyboards.confirmation import confirm_keyboard
from src.bot.keyboards.settings import get_setting_menu
from src.bot.state import BotCategorySettingsStates
from src.services.category import add_new_category_from_user, update_category_name_by_id, delete_category_by_id

category_router = Router()


@category_router.message(F.text.lower() == "category settings")
async def category_menu(message: Message, state: FSMContext) -> None:
    await message.answer("Category Menu", reply_markup=category_keyboard)
    await state.set_state(BotCategorySettingsStates.settings_category)


@category_router.message(F.text.lower() == "add category")
async def add_category(message: Message, state: FSMContext) -> None:
    await message.answer("Please enter the name of the category you want to add:")
    await message.answer("Or cancel the operation:", reply_markup=cancel_keyboard)
    await state.set_state(BotCategorySettingsStates.add_category)


@category_router.message(StateFilter(BotCategorySettingsStates.add_category))
async def adding_new_category(message: Message, state: FSMContext) -> None:
    answer = await add_new_category_from_user(message.from_user.id, message.text)
    await message.answer(answer, reply_markup=category_keyboard)
    await state.set_state(BotCategorySettingsStates.settings_category)


@category_router.message(F.text.lower() == "edit category")
async def edit_category(message: Message, state: FSMContext) -> None:
    keyboard = await get_categories_keyboard(message.from_user.id, "edit_category")
    await message.answer("Choose a category to edit:", reply_markup=keyboard)
    await message.answer("Or cancel the operation:", reply_markup=cancel_keyboard)
    await state.set_state(BotCategorySettingsStates.edit_category)


@category_router.callback_query(F.data.startswith("edit_category_"),
                                StateFilter(BotCategorySettingsStates.edit_category))
async def handle_category_edit_selection(callback_query: CallbackQuery, state: FSMContext):
    category_id = int(callback_query.data.split("_")[2])
    await state.set_state(BotCategorySettingsStates.new_name_for_category)
    await state.update_data(category_id=category_id)
    await callback_query.message.answer("Enter new name :")


@category_router.message(StateFilter(BotCategorySettingsStates.new_name_for_category))
async def handle_new_category_name(message: Message, state: FSMContext):
    new_category_name = message.text
    user_data = await state.get_data()
    await update_category_name_by_id(user_data['category_id'], new_category_name)
    await message.answer(f"Category name updated to: {new_category_name}", reply_markup=category_keyboard)
    await state.clear()
    await state.set_state(BotCategorySettingsStates.settings_category)


@category_router.message(F.text.lower() == "delete category")
async def delete_category_list(message: Message, state: FSMContext) -> None:
    keyboard = await get_categories_keyboard(message.from_user.id, "delete_category")
    await message.answer("Choose a category to delete:", reply_markup=keyboard)
    await state.set_state(BotCategorySettingsStates.delete_category)


@category_router.callback_query(F.data.startswith("delete_category_"),
                                StateFilter(BotCategorySettingsStates.delete_category))
async def handle_category_selection_deletion(callback_query: CallbackQuery, state: FSMContext):
    category_id = int(callback_query.data.split("_")[2])
    await state.set_state(BotCategorySettingsStates.deletion_confirm)
    await state.update_data(category_id=category_id)
    await callback_query.message.answer("Confirm deletion :", reply_markup=confirm_keyboard)


@category_router.message(F.text.lower() == "confirm", StateFilter(BotCategorySettingsStates.deletion_confirm))
async def deletion_of_category(message: Message, state: FSMContext):
    user_data = await state.get_data()
    await delete_category_by_id(user_data['category_id'])
    await message.answer("Category deleted", reply_markup=category_keyboard)
    await state.clear()
    await state.set_state(BotCategorySettingsStates.settings_category)


@category_router.message(F.text.lower() == "back to settings")
async def back_to_settings(message: Message) -> None:
    await message.answer("Settings Menu", reply_markup=await get_setting_menu(message.from_user.id))


@category_router.message(F.text.lower() == "cancel", StateFilter(BotCategorySettingsStates.edit_category,
                                                                 BotCategorySettingsStates.new_name_for_category,
                                                                 BotCategorySettingsStates.deletion_confirm))
async def cancel_editing_category(message: Message, state: FSMContext) -> None:
    await state.set_state(BotCategorySettingsStates.settings_category)
    await message.answer("Operation was canceled", reply_markup=category_keyboard)
