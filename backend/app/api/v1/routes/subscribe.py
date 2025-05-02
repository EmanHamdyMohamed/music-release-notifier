from fastapi import APIRouter, HTTPException, Query
from app.models.user import UserIn
from app.db.mongo import db
from app.models.user_update import UpdateTelegramID, UpdatePhoneNumber

router = APIRouter()

@router.post("/subscribe")
async def subscribe(user: UserIn):
    existing = await db.users.find_one({"email": user.email})
    if existing:
        update_fields = {
            "subscribed_artists": [a.dict() for a in user.subscribed_artists]
        }
        # updates = {
        #     "$set": {
        #         "subscribed_artists": [a.dict() for a in user.subscribed_artists]
        #     }
        # }
        if user.notification_methods:
            update_fields["notification_methods"] = user.notification_methods
        if user.telegram_chat_id:
            update_fields["telegram_chat_id"] = user.telegram_chat_id
        if user.phone_number:
            update_fields["phone_number"] = user.phone_number

        # if update_fields:
        #     updates["$set"] = update_fields            

        # Update the user's subscriptions
        await db.users.update_one({"email": user.email}, {
            "$set": update_fields
        })
    else:
        # Create new user with subscriptions
        await db.users.insert_one(user.dict())

    return {"message": "Subscription updated"}

@router.get("/subscribe")
async def get_subscribe(email: str = Query()):
    if not email:
        raise HTTPException(status_code=400, detail="Email is required")
    existing = await db.users.find_one({"email": email})
    if not existing:
        return {"message": "User not found"}
    return {
        "email": existing["email"],
        "subscribed_artists": existing["subscribed_artists"],
        "notification_methods": existing["notification_methods"],
        "telegram_chat_id": existing["telegram_chat_id"],
        "phone_number": existing["phone_number"]
    }


@router.post("/update-telegram-id")
async def update_telegram_id(data: UpdateTelegramID):
    result = await db.users.update_one(
        {"email": data.email},
        {"$set": {"telegram_chat_id": data.telegram_chat_id}}
    )

    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="User not found")

    return {"message": "Telegram ID updated successfully"}


@router.post("/update-phone-number")
async def update_phone_number(data: UpdatePhoneNumber):
    result = await db.users.update_one(
        {"email": data.email},
        {"$set": {"phone_number": data.phone_number}}
    )

    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="User not found")

    return {"message": "Phone number updated successfully"}