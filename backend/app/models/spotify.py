from pydantic import BaseModel, Field
from typing import List, Optional


class Artist(BaseModel):
    id: str = Field(..., example="1Xyo4u8uXC1ZmMpatF05PJ")
    name: str = Field(..., example="The Weeknd")
    genres: List[str] = Field(default=[], example=["rnb", "pop"])
    popularity: Optional[int] = Field(default=None, example=85)
    image_url: Optional[str] = Field(default=None, example="https://i.scdn.co/image/abc123")


class SearchArtistsResponse(BaseModel):
    artists: List[Artist]
