from src.database.database import get_session
from src.database.models import User
from src.repository.user import add_user
from src.utils.generate_id import generate_user_id


class UserFactory:
    @staticmethod
    async def create_user(tg_user_id: int, tg_chat_id: int) -> str:
        async with get_session() as session:
            token = generate_user_id()
            await add_user(session, User(tg_user_id=tg_user_id, tg_chat_id=tg_chat_id, token=token))
        return token
