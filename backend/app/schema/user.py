# Pydantic models for API requests/responses (keep existing ones)
from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional
from datetime import datetime
from app.models.mongoengine_models import User


class ArtistSubscription(BaseModel):
    """Artist subscription embedded document"""
    id: str = Field(example="1Xyo4u8uXC1ZmMpatF05PJ")
    name: Optional[str] = Field(example="The Weeknd")
    url: Optional[str] = Field(example="https://open.spotify.com/artist/1Xyo4u8uXC1ZmMpatF05")


class UserIn(BaseModel):
    """User input model for API"""
    email: EmailStr = Field(example="user@example.com")
    subscribed_artists: Optional[List[ArtistSubscription]] = Field(default=[])
    notification_methods: Optional[List[str]] = Field(default=[], example=["telegram", "sms"])
    telegram_chat_id: Optional[str] = Field(default=None, example="123456789")
    phone_number: Optional[str] = Field(default=None, example="+201234567890")


class UserOut(BaseModel):
    """User output model for API"""
    email: EmailStr = Field(..., example="user@example.com")
    subscribed_artists: Optional[List[ArtistSubscription]] = Field()
    notification_methods: Optional[List[str]] = Field(default=[], example=["telegram", "sms"])
    telegram_chat_id: Optional[str] = Field(default=None, example="123456789")
    phone_number: Optional[str] = Field(default=None, example="+201234567890")
    created_at: Optional[datetime] = Field()
    updated_at: Optional[datetime] = Field()

    @classmethod
    def from_user(cls, user: User) -> "UserOut":
        """Create UserOut from User document"""
        return cls(
            email=user.email,
            subscribed_artists=[ArtistSubscription(
                id=artist.id,
                name=artist.name,
                url=artist.url
            ) for artist in user.subscribed_artists],
            notification_methods=user.notification_methods,
            telegram_chat_id=user.telegram_chat_id,
            phone_number=user.phone_number,
            created_at=user.created_at,
            updated_at=user.updated_at
        )
