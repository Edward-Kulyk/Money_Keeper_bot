from pydantic import BaseModel, Field


class NotificationData(BaseModel):
    title: str = Field(..., example="NEU*Dallmayr Vending")
    text: str = Field(..., example="CZK45.00 with Visa •••• 4670")
    telegramNick: str = Field(..., example="edward")
    appName: str = Field(..., example="Google Play services")
