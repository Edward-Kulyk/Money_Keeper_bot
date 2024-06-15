from pydantic import BaseModel, Field


class NotificationData(BaseModel):
    title: str = Field(..., examples=["NEU*Dallmayr Vending"])
    text: str = Field(..., examples=["CZK45.00 with Visa •••• 4670"])
    telegramNick: str = Field(..., examples=["edward"])
    appName: str = Field(..., examples=["Google Play services"])
