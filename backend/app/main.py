from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.main import api_router
from app.core.config import settings
from app.db import base  # noqa: F401
from app.db.session import Base, engine


def create_tables():
    Base.metadata.create_all(bind=engine)


def create_application() -> FastAPI:
    application = FastAPI(title=settings.PROJECT_NAME)
    
    # Настройка CORS
    application.add_middleware(
        CORSMiddleware,
        allow_origins=settings.BACKEND_CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
        allow_headers=["*"],
        expose_headers=["*"],
    )
    
    application.include_router(api_router)
    return application


app = create_application()


@app.on_event("startup")
def on_startup():
    create_tables()