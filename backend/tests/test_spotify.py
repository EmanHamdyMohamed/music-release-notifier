import pytest
from unittest.mock import AsyncMock
from app.core.spotify_client import SpotifyClient

@pytest.mark.asyncio
async def test_get_new_releases(monkeypatch):
    fake_data = {"albums": {"items": [{"name": "Test Album"}]}}

    client = SpotifyClient()
    client._get_access_token = AsyncMock(return_value="fake-token")
    client.request_with_retry = AsyncMock(return_value=fake_data)

    result = await client.get_new_releases()
    assert result == fake_data
    client.request_with_retry.assert_called_once()
