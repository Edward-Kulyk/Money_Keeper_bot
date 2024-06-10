from aiogram import F, Router, types
from src.bot.keyboards.main_menu import main_menu_keyboard
from src.bot.keyboards.settings import settings_keyboard
from src.services.user import get_user_token
from src.utils.factories.user import UserFactory

settings_router = Router()


@settings_router.message(F.text.lower() == "settings")
async def settings_menu(message: types.Message) -> None:
    await message.answer("Settings Menu", reply_markup=settings_keyboard)


@settings_router.message(F.text.lower() == "get token")
async def get_token(message: types.Message) -> None:
    token = await get_user_token(str(message.from_user.id))
    if not token:
        token = await UserFactory.create_user(str(message.from_user.id), str(message.chat.id))
    await message.answer(f"Your token is: {token}")


@settings_router.message(F.text.lower() == "back to main menu")
async def back_to_main_menu(message: types.Message) -> None:
    await message.answer("Main Menu", reply_markup=main_menu_keyboard)
