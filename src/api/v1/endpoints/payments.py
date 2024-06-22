from fastapi import APIRouter, HTTPException
from starlette import status

from src.schemas.android_app import NotificationData
from src.services.operation import parse_notification
from src.services.user import get_user_by_tg_token

router = APIRouter()


@router.post("/notifications", status_code=status.HTTP_200_OK)
async def get_notification_from_user(data: NotificationData) -> dict[str, str]:
    # Change after key  update in app
    print(data)
    user = await get_user_by_tg_token(str(data.telegramNick))
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    await parse_notification(data, user.id)
    return {"status": "success", "message": "Notification received"}
