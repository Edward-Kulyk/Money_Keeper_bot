from pydantic import BaseModel, Field
from pydantic.v1 import validator, root_validator

from src.services.user import get_user_by_tg_token


class NotificationData(BaseModel):
    title: str = Field(..., examples=["NEU*Dallmayr Vending"])
    text: str = Field(..., examples=["CZK45.00 with Visa •••• 4670"])
    telegramNick: str = Field(..., examples=["edward"])
    appName: str = Field(..., examples=["Google Play services"])

    @validator('title')
    def validate_title(self, value):
        if not value:
            raise ValueError('Title must not be empty')
        return value

    @validator('appName')
    def validate_app_name(self, value):
        allowed_apps = ["Google Play services", "Google\xa0Wallet"]
        if value not in allowed_apps:
            raise ValueError(f'AppName must be one of {allowed_apps}')
        return value
