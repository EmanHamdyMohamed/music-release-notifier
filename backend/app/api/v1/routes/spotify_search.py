from fastapi import APIRouter, Query
from app.core.spotify_client import SpotifyClient

router = APIRouter()
spotify_client = SpotifyClient()


@router.get("/search_artists")
async def search(q: str = Query()):
    artists = await spotify_client.search_artists(q)
    return artists

