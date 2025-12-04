from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class ArticleBase(BaseModel):
    title: str
    content: str
    author: str


class ArticleCreate(BaseModel):
    title: str
    content: Optional[str] = None
    author: Optional[str] = None


class ArticleUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    author: Optional[str] = None


class ArticleRead(BaseModel):
    id: int
    title: str
    content: Optional[str] = None
    author: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

