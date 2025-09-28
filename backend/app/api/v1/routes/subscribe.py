from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import JSONResponse
from app.models.mongoengine_models import User, ArtistSubscription as MongoEngineArtistSubscription
from app.schema.user import UserIn, UserOut
from fastapi import status
from app.models.user_update import UpdateTelegramID, UpdatePhoneNumber
from app.models.user_response import UserResponse
from app.models.response import MessageResponse
from datetime import datetime

router = APIRouter(tags=["Subscription"])


@router.post(
    "/subscribe",
    summary="Subscribe or update user preferences",
    description="Creates a new user subscription or updates an existing user's artist list and notification preferences.",
    response_description="Confirmation of subscription update",
    status_code=status.HTTP_200_OK,
)
async def subscribe(user: UserIn):
    # Check if user exists
    existing_user = User.objects(email=user.email).first()
    
    # Convert Pydantic ArtistSubscription to MongoEngine ArtistSubscription
    mongoengine_artists = [
        MongoEngineArtistSubscription(
            id=artist.id,
            name=artist.name or "",
            url=artist.url
        ) for artist in (user.subscribed_artists or [])
    ]
    
    if existing_user:
        # Update existing user
        existing_user.subscribed_artists = mongoengine_artists
        existing_user.notification_methods = user.notification_methods or []
        existing_user.telegram_chat_id = user.telegram_chat_id
        existing_user.phone_number = user.phone_number
        
        existing_user.save()
        return JSONResponse(content={"message": "User preferences updated successfully"}, status_code=200)
    else:
        # Create new user
        new_user = User(
            email=user.email,
            subscribed_artists=mongoengine_artists,
            notification_methods=user.notification_methods or [],
            telegram_chat_id=user.telegram_chat_id,
            phone_number=user.phone_number
        )
        
        new_user.save()
        return JSONResponse(content={"message": "User subscribed successfully"}, status_code=201)


@router.get(
    "/subscribe",
    summary="Get user subscription details",
    description="Fetch subscription and notification preferences for a specific user by email.",
    responses={404: {"description": "User not found"}},
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
)
async def get_subscribe(
    email: str = Query(description="The user's email address")
):
    if not email:
        raise HTTPException(status_code=400, detail="Email is required")
    
    user = User.objects(email=email).first()
    print('user ====> ', user)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return UserOut.from_user(user)


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
async def update_telegram_id(data: UpdateTelegramID):
    user = User.objects(email=data.email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.telegram_chat_id = data.telegram_chat_id
    user.updated_at = datetime.utcnow()
    await user.save()

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
async def update_phone_number(data: UpdatePhoneNumber):
    user = User.objects(email=data.email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.phone_number = data.phone_number
    user.updated_at = datetime.utcnow()
    await user.save()

    return JSONResponse(content={"message": "Phone number updated successfully"}, status_code=200)