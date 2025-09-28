from typing import List
from fastapi import APIRouter
from app.models.beanie_models import Notification

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
    notifications = await Notification.find_all().sort("-sent_at").limit(100).to_list()
    return notifications
