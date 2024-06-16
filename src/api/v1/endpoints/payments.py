from fastapi import APIRouter

from src.schemas.android_app import NotificationData
from src.services.operation import parse_notification
from src.services.user import get_user_by_tg_token

router = APIRouter()


@router.post("/notifications")
async def get_notification_from_user(data: NotificationData) -> dict:
    # Change after key  update in app
    print(data)
    user = await get_user_by_tg_token(str(data.telegramNick))
    if not user:
        return {"status": "error", "message": "User not found"}
    if data.appName == "Google\xa0Wallet":
        await parse_notification(data, user.id)
        return {"status": "success", "message": "Notification received"}
    else:
        return {"status": "error", "message": "Posel nahui"}
