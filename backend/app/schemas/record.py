from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class RecordBase(BaseModel):
    user_id: int
    article_id: int
    title: str
    content: str


class RecordCreate(RecordBase):
    pass


class RecordUpdate(BaseModel):
    user_id: Optional[int] = None
    article_id: Optional[int] = None
    title: Optional[str] = None
    content: Optional[str] = None


class RecordRead(RecordBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

