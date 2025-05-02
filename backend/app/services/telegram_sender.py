from app.core.config import settings
from telegram import Bot

async def send_telegram_message(chat_id: str, message: str):
    async with Bot(token=settings.telegram_bot_token) as bot:
        await bot.send_message(text=message, chat_id=chat_id)