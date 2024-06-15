from aiogram import F, Router, types
from src.bot.keyboards.main_menu import main_menu_keyboard
from src.bot.keyboards.settings import get_setting_menu

from src.services.user import get_user_token, update_user_payment_mode_by_tg_id
from src.utils.factories.user import UserFactory

settings_router = Router()


@settings_router.message(F.text.lower() == "settings")
async def settings_menu(message: types.Message) -> None:
    await message.answer("Settings Menu", reply_markup=await get_setting_menu(message.from_user.id))


@settings_router.message(F.text.lower() == "get token")
async def get_token(message: types.Message) -> None:
    token = await get_user_token(message.from_user.id)
    if not token:
        token = await UserFactory.create_user(message.from_user.id, message.chat.id)
    await message.answer(f"Your token is: {token}")


@settings_router.message(F.text.lower().in_({"payments mode: remember", "payments mode: not save"}))
async def switch__user_mode(message: types.Message) -> None:
    await update_user_payment_mode_by_tg_id(message.from_user.id)
    await message.answer("Settings Menu", reply_markup=await get_setting_menu(message.from_user.id))
