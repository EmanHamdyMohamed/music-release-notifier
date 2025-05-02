from unittest.mock import patch
from app.services.email_sender import send_email

@patch("app.services.email_sender.aiohttp.ClientSession.post")
async def test_send_email(mock_post):
    mock_post.return_value.__aenter__.return_value.status = 200
    await send_email("test@example.com", "Subject", "Body")
    mock_post.assert_called()