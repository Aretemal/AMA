from fastapi import APIRouter

from app.api.routes import albums, articles, auth, songs
from app.core.config import settings

api_router = APIRouter(prefix=settings.API_V1_STR)

api_router.include_router(auth.router)
api_router.include_router(articles.router)
api_router.include_router(songs.router)
api_router.include_router(albums.router)