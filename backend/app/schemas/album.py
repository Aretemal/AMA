from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel


class AlbumBase(BaseModel):
    title: str


class AlbumCreate(BaseModel):
    title: str
    creator: str
    song_ids: List[int]


class AlbumUpdate(BaseModel):
    title: Optional[str] = None
    creator: Optional[str] = None
    song_ids: Optional[List[int]] = None


class AlbumRead(BaseModel):
    id: int
    title: Optional[str] = None
    creator: Optional[str] = None
    song_ids: Optional[List[int]] = None
    user_ids: Optional[List[int]] = None

    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}

