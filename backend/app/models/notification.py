from pydantic import BaseModel, EmailStr, Field
from typing import List, Literal, Optional
from datetime import datetime


class Notification(BaseModel):
    email: EmailStr
    artist_ids: List[str]
    album_id: str
    method: Literal["email", "telegram", "sms"]
    sent_at: datetime = Field(default_factory=datetime.utcnow)
    spotify_url: str
    telegram_chat_id: Optional[str] = None
    phone_number: Optional[str] = None
    matched_artist_ids: Optional[List[str]] = None
