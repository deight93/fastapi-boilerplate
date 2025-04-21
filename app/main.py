from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from httpx import AsyncClient
from sqladmin import Admin

from app.admin.auth import authentication_admin
from app.admin.views import UserAdmin
from app.core.database import engine
from app.core.logger import logging
from app.core.metadata import swagger_metadata
from app.core.setting import settings
from app.routers import auth, user


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[dict[str, AsyncClient]]:
    logging.info(
        f"INFO:     Hello, Run the server in the {settings.ENV_STATE} environment 👋"
    )
    yield
    logging.info(
        f"INFO:     Bye, Shut down the server in the {settings.ENV_STATE} environment 👋"
    )


app = FastAPI(**swagger_metadata, lifespan=lifespan, debug=True)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user.router)
app.include_router(auth.router)

admin = Admin(app, engine, authentication_backend=authentication_admin)
admin.add_view(UserAdmin)


@app.get("/file-logging-test")
async def file_logging_test():
    logger = logging.getLogger(__name__)
    logger.info("logging test ...")

    return {"logging_check": "logging success"}


@app.get("/api-health-check")
async def api_health_check():
    return {
        "api_health_check": "api-server is Ok",
        "debug-mode": settings.DEBUG,
    }


app.mount("/static", StaticFiles(directory="app/core/static"), name="static")
