"""
MongoEngine ODM models for MongoDB
"""
from mongoengine import (
    Document,
    EmbeddedDocument,
    EmailField,
    EmbeddedDocumentField,
    ListField,
    StringField,
    DateTimeField
)
from datetime import datetime


class ArtistSubscription(EmbeddedDocument):
    """Artist subscription embedded document"""
    id = StringField(required=True)
    name = StringField(required=True)
    url = StringField(required=False, default=None)


class User(Document):
    """User document model"""
    email = EmailField(required=True, unique=True, example="user@example.com")
    subscribed_artists = ListField(EmbeddedDocumentField(ArtistSubscription), default=list, required=False)
    notification_methods = ListField(StringField(), default=list, example=["telegram", "sms"])
    telegram_chat_id = StringField(example="123456789")
    phone_number = StringField(example="+201234567890")
    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField(default=datetime.utcnow)

    meta = {
        'collection': 'users',
        'indexes': [
            'email',
            'created_at',
        ]
    }

    def __str__(self) -> str:
        return f"User(email={self.email})"

    def save(self, *args, **kwargs):
        """Override save to update updated_at timestamp"""
        self.updated_at = datetime.utcnow()
        return super().save(*args, **kwargs)


class Notification(Document):
    """Notification document model"""
    email = EmailField(required=True, example="user@example.com")
    album_id = StringField(required=True, example="4uLU6hMCjMI75M1A2tKUQC")
    album_name = StringField(required=True, example="Dawn FM")
    album_artists_ids = ListField(StringField(), default=list)
    method = StringField(required=True, choices=['email', 'telegram', 'sms'], example="email")
    sent_at = DateTimeField(default=datetime.utcnow)
    spotify_url = StringField(required=True, example="https://open.spotify.com/album/4uLU6hMCjMI75M1A2tKUQC")
    telegram_chat_id = StringField(example="123456789")
    phone_number = StringField(example="+201234567890")
    matched_artist_ids = ListField(StringField())

    meta = {
        'collection': 'notifications',
        'indexes': [
            'email',
            'album_id',
            'sent_at',
            [('email', 1), ('album_id', 1), ('method', 1)],  # Compound index
        ]
    }

    def __str__(self) -> str:
        return f"Notification(email={self.email}, album={self.album_name})"

