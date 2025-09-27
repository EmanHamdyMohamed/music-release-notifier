from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional


class ArtistSubscription(BaseModel):
    id: str = Field(..., example="1Xyo4u8uXC1ZmMpatF05PJ")
    name: str = Field(..., example="The Weeknd")
    url: Optional[str] = Field(default=None, example="https://open.spotify.com/artist/1Xyo4u8uXC1ZmMpatF05")


class UserIn(BaseModel):
    email: EmailStr = Field(..., example="user@example.com")
    subscribed_artists: List[ArtistSubscription]
    notification_methods: Optional[List[str]] = Field(default=[], example=["telegram", "sms"])
    telegram_chat_id: Optional[str] = Field(default=None, example="123456789")
    phone_number: Optional[str] = Field(default=None, example="+201234567890")


class UserInDB(UserIn):
    id: Optional[str] = Field(alias="_id", default=None)


class UserOut(BaseModel):
    email: EmailStr = Field(..., example="user@example.com")
    subscribed_artists: List[ArtistSubscription]
    notification_methods: List[str] = Field(default=[], example=["telegram", "sms"])
    telegram_chat_id: Optional[str] = Field(default=None, example="123456789")
    phone_number: Optional[str] = Field(default=None, example="+201234567890")
