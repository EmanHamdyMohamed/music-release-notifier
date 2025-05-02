from fastapi import APIRouter
from app.db.mongo import db

router = APIRouter()

@router.get("/notifications")
async def list_notifications():
    docs = await db.notifications.find().sort("sent_at", -1).to_list(length=100)
    return docs
