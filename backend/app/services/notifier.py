from app.models.mongoengine_models import User, Notification
from app.core.spotify_client import SpotifyClient
from app.services.email_sender import send_email
from app.services.telegram_sender import send_telegram_message
from app.services.sms_sender import send_sms
from app.utils.logger import get_logger
from app.models.notification import Notification
import textwrap

logger = get_logger(__name__)
spotify_client = SpotifyClient()


async def save_notification(
    notification_method: str,
    user_email: str,
    album_artists_ids: list,
    album: dict,
    user: dict = None,  # optional user data for telegram and sms notifications (if provided)
    matched_artist_ids: list = None  # optional for telegram and sms notifications (if provided)
):
    notification_doc = Notification(
        email=user_email,
        artist_ids=album_artists_ids,
        album_id=album["id"],
        method=notification_method,
        spotify_url=album["external_urls"]["spotify"],
        telegram_chat_id=user.get("telegram_chat_id"),
        phone_number=user.get("phone_number"),
        matched_artist_ids=matched_artist_ids
    )

    # Create notification document
    notification = Notification(
        email=notification_doc.email,
        album_id=notification_doc.album_id,
        album_name=notification_doc.album_name,
        album_artists_ids=notification_doc.album_artists_ids,
        method=notification_doc.method,
        spotify_url=notification_doc.spotify_url,
        telegram_chat_id=notification_doc.telegram_chat_id,
        phone_number=notification_doc.phone_number,
        matched_artist_ids=notification_doc.matched_artist_ids
    )
    notification.save()


async def check_notifications_sent(notification_method: str, user_email: str, album_id: str):
    notification = Notification.objects(
        email=user_email,
        album_id=album_id,
        method=notification_method
    ).first()
    return notification is not None


async def check_new_releases_and_notify():
    logger.info("Checking for new releases... 🎵")
    try:
        # 1. Get all users from the database
        users = list(User.objects.all())
        print('Users: ', users)

        # 2. Get latest Spotify releases
        new_releases_data = await spotify_client.get_new_releases()
        print(new_releases_data)
        albums = new_releases_data["albums"]["items"]

        notifications_sent = 0
        for user in users:
            user_email = user["email"]
            subscribed_artists = {artist["id"] for artist in user["subscribed_artists"]}
            preferred_methods = user.get("notification_methods", ["email"])  # default to email

            for album in albums:
                album_artists_ids = {artist["id"] for artist in album["artists"]}
                matched_artist_ids = album_artists_ids.intersection(subscribed_artists)
                if not album_artists_ids or not matched_artist_ids:
                    continue

                artist_names = [a['name'] for a in album["artists"] if a["id"] in subscribed_artists]

                subject = f"🎵 New Release: {artist_names} just dropped {album['name']}!"
                body = textwrap.dedent(f"""
                    Hi there!

                    🎵 New Album Released: {album['name']}
                    👤 By: {', '.join(artist_names)} (matched your subscriptions)
                    📅 Release Date: {album['release_date']}

                    🎧 Listen on Spotify:
                    {album['external_urls']['spotify']}

                    Enjoy the music! 🎶
                """)

                if "email" in preferred_methods:
                    exists = await check_notifications_sent("email", user_email, album["id"])
                    if not exists:
                        await send_email(user_email, subject, body)
                        await save_notification("email", user_email, album_artists_ids, album, user, matched_artist_ids)
                        notifications_sent += 1

                if "telegram" in preferred_methods and user.get("telegram_chat_id"):
                    exists = await check_notifications_sent("telegram", user_email, album["id"])
                    if not exists:
                        await send_telegram_message(user["telegram_chat_id"], body)
                        await save_notification("telegram", user_email, album_artists_ids, album, user, matched_artist_ids)
                        notifications_sent += 1
                    
                if "sms" in preferred_methods and user.get("phone_number"):
                    print('Attempting to send SMS...')
                    exists = await check_notifications_sent("sms", user_email, album["id"])
                    print('exists: ', exists)
                    if not exists:
                        send_sms(user["phone_number"], body)
                        await save_notification("sms", user_email, album_artists_ids, album, user, matched_artist_ids)
                        notifications_sent += 1
        logger.info(f"✅ Sent {notifications_sent} notifications.")
    except Exception as e:
        logger.exception("Error checking new releases:", exc_info=e)
