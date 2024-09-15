from aiogram import F, Router
from aiogram.types import Message

from src.bot.keyboards.settings import get_setting_menu
from src.services.user import get_user_token, update_user_payment_mode_by_tg_id
from src.utils.factories.user import UserFactory

settings_router = Router()


@settings_router.message(F.text.lower() == "settings")
async def settings_menu(message: Message) -> None:
    if message.from_user:
        await message.answer("Settings Menu", reply_markup=await get_setting_menu(message.from_user.id))
    else:
        await message.answer("User information not available.")


@settings_router.message(F.text.lower() == "get token")
async def get_token(message: Message) -> None:
    if message.from_user:
        token = await get_user_token(message.from_user.id)
        if not token:
            token = await UserFactory.create_user(message.from_user.id, message.chat.id)
        await message.answer(f"Your token is: {token}")
    else:
        await message.answer("User information not available.")


@settings_router.message(F.text.lower().in_({"payments mode: remember", "payments mode: not save"}))
async def switch_user_mode(message: Message) -> None:
    if message.from_user:
        await update_user_payment_mode_by_tg_id(message.from_user.id)
        await message.answer("Settings Menu", reply_markup=await get_setting_menu(message.from_user.id))
    else:
        await message.answer("User information not available.")
