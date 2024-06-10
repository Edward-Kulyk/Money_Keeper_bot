from fastapi import APIRouter
from src.schemas.android_app import NotificationData

router = APIRouter()


@router.post("/notifications")
def get_notification_from_user(data: NotificationData) -> dict:
    print(data)

    return {"status": "success", "message": "Notification received"}
