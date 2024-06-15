from src.database.database import get_session
from src.repository.user import get_user_by_tg_user_id, get_user_payment_mode, update_payment_mode


async def get_user_token(tg_user_id: int) -> str | None:
    async with get_session() as session:
        user = await get_user_by_tg_user_id(session, tg_user_id)
        if user:
            return user.token
        return


async def get_user_payment_mode_by_tg_id(tg_user_id: int) -> str:
    async with get_session() as session:
        return await get_user_payment_mode(session, tg_user_id)


async def update_user_payment_mode_by_tg_id(tg_user_id: int) -> None:
    async with get_session() as session:
        user = await get_user_by_tg_user_id(session, tg_user_id)
        new_mode = "not save" if user.payment_mode == "remember" else "remember"
        await update_payment_mode(session, tg_user_id, new_mode)
