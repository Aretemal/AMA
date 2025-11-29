from fastapi import FastAPI

from app.api.main import api_router
from app.core.config import settings
from app.db import base  # noqa: F401
from app.db.session import Base, engine


def create_tables():
    Base.metadata.create_all(bind=engine)


def create_application() -> FastAPI:
    application = FastAPI(title=settings.PROJECT_NAME)
    application.include_router(api_router)
    return application


app = create_application()


@app.on_event("startup")
def on_startup():
    create_tables()