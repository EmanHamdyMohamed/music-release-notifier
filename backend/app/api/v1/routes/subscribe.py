from fastapi import APIRouter, HTTPException, Query, Depends
from fastapi.responses import JSONResponse
from app.models.user import UserIn, UserOut
from app.db.mongo import get_db
from fastapi import status
from app.models.user_update import UpdateTelegramID, UpdatePhoneNumber
from app.models.user_response import UserResponse
from app.models.response import MessageResponse
from motor.motor_asyncio import AsyncIOMotorDatabase

router = APIRouter(tags=["Subscription"])


@router.post(
    "/subscribe",
    summary="Subscribe or update user preferences",
    description="Creates a new user subscription or updates an existing user's artist list and notification preferences.",
    response_description="Confirmation of subscription update",
    status_code=status.HTTP_200_OK,
)
async def subscribe(user: UserIn, db: AsyncIOMotorDatabase = Depends(get_db)):
    existing = await db.users.find_one({"email": user.email})
    if existing:
        update_fields = {
            "subscribed_artists": [a.dict() for a in user.subscribed_artists]
        }
        if user.notification_methods:
            update_fields["notification_methods"] = user.notification_methods
        if user.telegram_chat_id:
            update_fields["telegram_chat_id"] = user.telegram_chat_id
        if user.phone_number:
            update_fields["phone_number"] = user.phone_number

        await db.users.update_one({"email": user.email}, {
            "$set": update_fields
        })
    else:
        await db.users.insert_one(user.dict())

    return JSONResponse(content={"message": "Subscription updated"}, status_code=200)


@router.get(
    "/subscribe",
    summary="Get user subscription details",
    description="Fetch subscription and notification preferences for a specific user by email.",
    responses={404: {"description": "User not found"}},
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
)
async def get_subscribe(
    email: str = Query(description="The user's email address"),
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    if not email:
        raise HTTPException(status_code=400, detail="Email is required")
    existing = await db.users.find_one({"email": email})
    if not existing:
        raise HTTPException(status_code=404, detail="User not found")

    return UserOut(**existing)


@router.post(
    "/update-telegram-id",
    summary="Update Telegram chat ID",
    description="Update the Telegram chat ID for an existing user by email.",
    response_description="Confirmation message",
    response_model=MessageResponse,
    responses={
        200: {"description": "Telegram ID updated successfully"},
        404: {"description": "User not found"},
    },
)
async def update_telegram_id(data: UpdateTelegramID, db: AsyncIOMotorDatabase = Depends(get_db)):
    result = await db.users.update_one(
        {"email": data.email},
        {"$set": {"telegram_chat_id": data.telegram_chat_id}}
    )

    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="User not found")

    return JSONResponse(content={"message": "Telegram ID updated successfully"}, status_code=200)


@router.post(
    "/update-phone-number",
    summary="Update phone number",
    description="Update the phone number for an existing user by email.",
    response_description="Confirmation message",
    response_model=MessageResponse,
    responses={
        200: {"description": "Phone number updated successfully"},
        404: {"description": "User not found"},
    },
)
async def update_phone_number(data: UpdatePhoneNumber, db: AsyncIOMotorDatabase = Depends(get_db)):
    result = await db.users.update_one(
        {"email": data.email},
        {"$set": {"phone_number": data.phone_number}}
    )

    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="User not found")
    return JSONResponse(content={"message": "Phone number updated successfully"}, status_code=200)