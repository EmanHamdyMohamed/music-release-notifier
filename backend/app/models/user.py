from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional


class ArtistSubscription(BaseModel):
    id: str
    name: str
    url: str = None


class UserIn(BaseModel):
    email: EmailStr
    subscribed_artists: List[ArtistSubscription]
    notification_methods: List[str] = Field(default=["email"])
    telegram_chat_id: str = None
    phone_number: str = None


class UserInDB(UserIn):
    id: Optional[str] = Field(alias="_id", default=None)
