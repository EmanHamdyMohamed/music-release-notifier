from pydantic_settings import BaseSettings
from dotenv import load_dotenv

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

    telegram_bot_token: str = ""

    twilio_account_sid: str
    twilio_auth_token: str
    twilio_phone_number: str

    class Config:
        env_file = ".env"

settings = Settings()
