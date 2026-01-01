from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class RecordBase(BaseModel):
    article_id: int
    content: Optional[str] = None
    type_record: Optional[str] = None
    options: Optional[dict] = None


class RecordCreate(BaseModel):
    article_id: int
    content: Optional[str] = None
    type_record: Optional[str] = None
    options: Optional[dict] = None


class RecordUpdate(BaseModel):
    article_id: Optional[int] = None
    content: Optional[str] = None
    type_record: Optional[str] = None
    options: Optional[dict] = None


class RecordRead(BaseModel):
    id: int
    article_id: int
    user_id: int
    content: Optional[str] = None
    type_record: Optional[str] = None
    options: Optional[dict] = None
    created_at: datetime

    model_config = {"from_attributes": True}

