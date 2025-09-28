import httpx
import base64
from app.core.config import settings
import asyncio
from app.utils.logger import get_logger
from datetime import datetime, timedelta

logger = get_logger(__name__)


class SpotifyClient:
    def __init__(self):
        self.client_id = settings.spotify_client_id
        self.client_secret = settings.spotify_client_secret
        self.token_url = "https://accounts.spotify.com/api/token"
        self.api_url = "https://api.spotify.com/v1"
        self.access_token = None
        self.expires_at = datetime.now()

    async def authenticate(self):
        if self.access_token and datetime.now() < self.expires_at:
            return self.access_token

        logger.info("Refreshing Spotify access token...")

        auth_header = base64.b64encode(f"{self.client_id}:{self.client_secret}".encode()).decode()
        headers = {
            "Authorization": f"Basic {auth_header}",
            "Content-Type": "application/x-www-form-urlencoded"
        }
        data = {"grant_type": "client_credentials"}

        async with httpx.AsyncClient() as client:
            response = await client.post(self.token_url, data=data, headers=headers)
            response.raise_for_status()
            token_info = response.json()
            self.access_token = token_info["access_token"]
            expires_in = token_info.get("expires_in", 3600)  # default 1 hour
            self.expires_at = datetime.now() + timedelta(seconds=expires_in)
        return self.access_token

    # add rety logic
    async def request_with_retry(self, url: str, headers: dict, params: dict = None, max_retries: int = 3):
        retries = 0
        while retries < max_retries:
            try:
                retries += 1
                async with httpx.AsyncClient() as client:
                    response = await client.get(url, headers=headers, params=params)
                    if response.status_code == 429:
                        logger.warning(f"Spotify rate limited. Retrying after {response.headers['Retry-After']} seconds.")
                        await asyncio.sleep(response.headers["Retry-After"])
                        continue
                    response.raise_for_status()
                    return response.json()
            except httpx.HTTPError as e:
                if retries >= max_retries:
                    raise e
                await asyncio.sleep(2 ** retries)
        logger.error(f"Failed to fetch from Spotify after {max_retries} attempts.")
        return None

    async def get_new_releases(self, country: str = "US", limit: int = 10):
        if not self.access_token:
            await self.authenticate()

        print(self.access_token)
        headers = {
            "Authorization": f"Bearer {self.access_token}"
        }

        releases = await self.request_with_retry(f"{self.api_url}/browse/new-releases", headers, params={"country": country, "limit": limit})
        return releases
    
    async def search_artists(self, keyword: str):
        # implment call spotify search
        if not self.access_token:
            await self.authenticate()
        headers = {
            "Authorization": f"Bearer {self.access_token}"
        }
        params = {
            "q": keyword,
            "type": "artist",
            "limit": 50,
            "market": "US"
        }
        data = await self.request_with_retry(
                f"{self.api_url}/search",
                headers=headers,
                params=params   
            )
        return [
            {
                "name": item["name"],
                "id": item["id"],
                "popularity": item['popularity'],
                "image_url": item["images"][0]["url"] if (item["images"] and len(item["images"]) > 0) else None
            }
            for item in data["artists"]["items"]
        ]
