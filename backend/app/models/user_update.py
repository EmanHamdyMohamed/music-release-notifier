from pydantic import BaseModel, EmailStr, Field


class UpdateTelegramID(BaseModel):
    email: EmailStr = Field(..., example="user@example.com", description="User's email")
    telegram_chat_id: str = Field(..., example="123456789", description="New Telegram chat ID")


class UpdatePhoneNumber(BaseModel):
    email: EmailStr = Field(..., example="user@example.com", description="User's email")
    phone_number: str = Field(..., example="+201234567890", description="New phone number")
