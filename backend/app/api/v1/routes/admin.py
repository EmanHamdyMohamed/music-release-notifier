from typing import List
from fastapi import APIRouter
from app.models.mongoengine_models import Notification
from app.schema.notification import NotificationOut

router = APIRouter(tags=["Notifications"])


@router.get(
    "/notifications",
    response_model=List[NotificationOut],
    summary="List recent notifications",
    description="Retrieve the latest 100 notifications sent to users, sorted by most recent first.",
    response_description="List of notification documents",
    tags=["Notifications"]
)
async def list_notifications():
    notifications = Notification.objects.order_by('-sent_at').limit(100)
    return list(notifications)
