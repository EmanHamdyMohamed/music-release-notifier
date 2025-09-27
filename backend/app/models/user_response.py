from pydantic import BaseModel
from typing import List, Optional
from app.models.user import ArtistSubscription


class UserResponse(BaseModel):
    email: str
    subscribed_artists: List[ArtistSubscription]
    notification_methods: Optional[List[str]]
    telegram_chat_id: Optional[str]
    phone_number: Optional[str]
