from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class ArticleBase(BaseModel):
    title: str
    author: Optional[str] = None


class ArticleCreate(BaseModel):
    title: str
    author: Optional[str] = None


class ArticleUpdate(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None


class ArticleRead(BaseModel):
    id: int
    title: str
    author: Optional[str] = None
    user_id: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}

