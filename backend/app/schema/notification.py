from pydantic import BaseModel, Field
from enum import Enum
from datetime import datetime


class NotificationMethod(Enum):
    email = 'email'
    telegram = 'telegram'
    sms = 'sms'


class NotificationOut(BaseModel):
    email: str = Field(example="user@example.com")
    album_id: str = Field(example="4uLU6hMCjMI75M1A2tKUQC")
    album_name: str = Field(example="Dawn FM")
    album_artists_ids: list[str] = Field(default=list)
    method: NotificationMethod = Field(choices=['email', 'telegram', 'sms'], example="email")
    sent_at: datetime = Field(default=datetime.utcnow)
    spotify_url: str = Field(example="https://open.spotify.com/album/4uLU6hMCjMI75M1A2tKUQC")
    telegram_chat_id: str = Field(example="123456789")
    phone_number: str = Field(example="+201234567890")
    matched_artist_ids: list[str] = Field()
    