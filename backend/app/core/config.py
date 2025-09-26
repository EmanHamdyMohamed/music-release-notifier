from pydantic_settings import BaseSettings
from dotenv import load_dotenv
from typing import List


# Load environment variables from .env file
load_dotenv()


class Settings(BaseSettings):
    # MongoDB settings
    mongo_uri: str = "mongodb://localhost:27017/"
    database_name: str = "music_notifier"

    # Spotify settings
    spotify_client_id: str = ""
    spotify_client_secret: str = ""

    # Email settings
    from_email: str = ""
    smtp_server: str = "smtp.gmail.com"
    smtp_port: int = "587"
    smtp_user: str = ""
    smtp_password: str = ""

    # Notification settings
    telegram_bot_token: str = ""
    twilio_account_sid: str = ""
    twilio_auth_token: str = ""
    twilio_phone_number: str = ""

    # Allow CORS origins to be overridden via environment variable
    # Format: "https://domain1.com,https://domain2.com"
    cors_origins_env: str = ""

    @property
    def get_cors_origins(self) -> List[str]:
        """Get CORS origins, with environment variable override support"""
        if self.cors_origins_env:
            return [origin.strip() for origin in
                    self.cors_origins_env.split(",")]
        return []

    class Config:
        env_file = ".env"


settings = Settings()
