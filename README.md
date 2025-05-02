# Music Release Notifier 🎧

Track your favorite Spotify artists and get notified by email, SMS, or Telegram when they release new music.

## Features
- Spotify artist search
- Email, Telegram, and SMS notifications
- User subscriptions saved to MongoDB
- APScheduler runs every hour to check new releases

## Tech Stack
- FastAPI + MongoDB (Motor)
- Vue 3 + Tailwind CSS
- Spotify API + SMTP + Telegram + Twilio

## Setup

### Backend
```bash
cd backend
poetry install
cp .env.example .env
poetry run uvicorn app.main:app --reload

### Frontend
```bash
cd frontend
npm install
npm run dev
```
