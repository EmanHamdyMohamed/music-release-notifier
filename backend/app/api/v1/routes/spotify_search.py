from fastapi import APIRouter, Query
from app.core.spotify_client import SpotifyClient
from app.models.spotify import SearchArtistsResponse

router = APIRouter(tags=["Spotify"])
spotify_client = SpotifyClient()


@router.get(
    "/search_artists",
    response_model=SearchArtistsResponse,
    summary="Search for artists on Spotify",
    description="Search for artists by name using the Spotify API.",
    response_description="List of matched artists",
    tags=["Spotify"]
)
async def search(q: str = Query(description="Artist name to search for")):
    artists = await spotify_client.search_artists(q)
    return {"artists": artists}
