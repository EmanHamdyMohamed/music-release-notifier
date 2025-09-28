from typing import List
from fastapi import APIRouter, Depends
from app.db.mongo import get_db
from app.models.notification import Notification
from motor.motor_asyncio import AsyncIOMotorDatabase

router = APIRouter(tags=["Notifications"])


@router.get(
    "/notifications",
    response_model=List[Notification],
    summary="List recent notifications",
    description="Retrieve the latest 100 notifications sent to users, sorted by most recent first.",
    response_description="List of notification documents",
    tags=["Notifications"]
)
async def list_notifications(db: AsyncIOMotorDatabase = Depends(get_db)):
    docs = await db.notifications.find().sort("sent_at", -1).to_list(length=100)
    return docs
