"""
Beanie ODM models for MongoDB
"""
from beanie import Document, Indexed
from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional, Literal
from datetime import datetime


class ArtistSubscription(BaseModel):
    """Artist subscription model"""
    id: str = Field(..., example="1Xyo4u8uXC1ZmMpatF05PJ")
    name: str = Field(..., example="The Weeknd")
    url: Optional[str] = Field(default=None, example="https://open.spotify.com/artist/1Xyo4u8uXC1ZmMpatF05")


class User(Document):
    """User document model"""
    email: Indexed(EmailStr, unique=True) = Field(..., example="user@example.com")
    subscribed_artists: List[ArtistSubscription] = Field(default_factory=list)
    notification_methods: List[str] = Field(default_factory=list, example=["telegram", "sms"])
    telegram_chat_id: Optional[str] = Field(default=None, example="123456789")
    phone_number: Optional[str] = Field(default=None, example="+201234567890")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "users"  # Collection name
        indexes = [
            "email",  # Single field index
            "created_at",  # Single field index
        ]

    def __str__(self) -> str:
        return f"User(email={self.email})"


class Notification(Document):
    """Notification document model"""
    email: Indexed(EmailStr) = Field(..., example="user@example.com")
    album_id: str = Field(..., example="4uLU6hMCjMI75M1A2tKUQC")
    album_name: str = Field(..., example="Dawn FM")
    album_artists_ids: List[str] = Field(default_factory=list)
    method: Literal["email", "telegram", "sms"] = Field(..., example="email")
    sent_at: datetime = Field(default_factory=datetime.utcnow)
    spotify_url: str = Field(..., example="https://open.spotify.com/album/4uLU6hMCjMI75M1A2tKUQC")
    telegram_chat_id: Optional[str] = Field(default=None, example="123456789")
    phone_number: Optional[str] = Field(default=None, example="+201234567890")
    matched_artist_ids: Optional[List[str]] = Field(default=None)

    class Settings:
        name = "notifications"  # Collection name
        indexes = [
            "email",  # Single field index
            "album_id",  # Single field index
            "sent_at",  # Single field index
            [("email", 1), ("album_id", 1), ("method", 1)],  # Compound index
        ]

    def __str__(self) -> str:
        return f"Notification(email={self.email}, album={self.album_name})"


# Pydantic models for API requests/responses (keep existing ones)
class UserIn(BaseModel):
    """User input model for API"""
    email: EmailStr = Field(..., example="user@example.com")
    subscribed_artists: List[ArtistSubscription]
    notification_methods: Optional[List[str]] = Field(default=[], example=["telegram", "sms"])
    telegram_chat_id: Optional[str] = Field(default=None, example="123456789")
    phone_number: Optional[str] = Field(default=None, example="+201234567890")


class UserOut(BaseModel):
    """User output model for API"""
    email: EmailStr = Field(..., example="user@example.com")
    subscribed_artists: List[ArtistSubscription]
    notification_methods: List[str] = Field(default=[], example=["telegram", "sms"])
    telegram_chat_id: Optional[str] = Field(default=None, example="123456789")
    phone_number: Optional[str] = Field(default=None, example="+201234567890")
    created_at: datetime
    updated_at: datetime

    @classmethod
    def from_user(cls, user: User) -> "UserOut":
        """Create UserOut from User document"""
        return cls(
            email=user.email,
            subscribed_artists=user.subscribed_artists,
            notification_methods=user.notification_methods,
            telegram_chat_id=user.telegram_chat_id,
            phone_number=user.phone_number,
            created_at=user.created_at,
            updated_at=user.updated_at
        )
