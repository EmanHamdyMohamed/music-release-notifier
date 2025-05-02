from pydantic import BaseModel, EmailStr


class UpdateTelegramID(BaseModel):
    email: EmailStr
    telegram_chat_id: str


class UpdatePhoneNumber(BaseModel):
    email: EmailStr
    phone_number: str

