from typing import List
from fastapi import APIRouter
from app.db.mongo import db
from app.models.notification import Notification

router = APIRouter(tags=["Notifications"])


@router.get(
    "/notifications",
    response_model=List[Notification],
    summary="List recent notifications",
    description="Retrieve the latest 100 notifications sent to users, sorted by most recent first.",
    response_description="List of notification documents",
    tags=["Notifications"]
)
async def list_notifications():
    docs = await db.notifications.find().sort("sent_at", -1).to_list(length=100)
    return docs
