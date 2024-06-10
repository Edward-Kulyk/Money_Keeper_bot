from src.database.database import get_session
from src.repository.user import get_user_by_tg_user_id


async def get_user_token(tg_user_id: str):
    async with get_session() as session:
        user = await get_user_by_tg_user_id(session, tg_user_id)
        if user:
            return user.token
        return
