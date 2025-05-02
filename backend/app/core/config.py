from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

class Settings(BaseSettings):
    # MongoDB settings
    mongo_uri: str = "mongodb://localhost:27017/"
    database_name: str = "music_notifier"
    
    # Spotify settings
    spotify_client_id: str = "7b7ddde7daea429d944b9180a3280411"
    spotify_client_secret: str = "145237c81909432bb36fd8ad16701afc"

    # Email settings
    from_email: str = "your_email@example.com"
    smtp_server: str = "smtp.gmail.com"
    smtp_port: int = "587"
    smtp_user: str = "your_email@example.com"
    smtp_password: str = "your_email_password"

    telegram_bot_token: str = "your_telegram_bot_token"

    twilio_account_sid: str
    twilio_auth_token: str
    twilio_phone_number: str

    class Config:
        env_file = ".env"

    # model_config = SettingsConfigDict(
    #     env_file=".env",
    #     env_file_encoding="utf-8",
    #     case_sensitive=True
    # )

settings = Settings()
