from twilio.rest import Client
from app.core.config import settings


def send_sms(to_phone: str, message: str):
    client = Client(settings.twilio_account_sid, settings.twilio_auth_token)

    message = client.messages.create(
        body=message,
        from_=settings.twilio_phone_number,
        to=to_phone
    )
    print(message.sid)
