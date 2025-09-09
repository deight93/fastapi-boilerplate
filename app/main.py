import logging
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

import logfire
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from httpx import AsyncClient
from scalar_fastapi import (
    SearchHotKey,
    get_scalar_api_reference,
)
from sqladmin import Admin

from app.admin.auth import authentication_admin
from app.admin.views import AdminTable
from app.core.database import engine
from app.core.exceptions import (
    AppError,
    app_exception_handler,
)
from app.core.metadata import swagger_metadata
from app.core.setting import settings
from app.routers import auth, item, user


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

if settings.LOGFIRE_TOKEN:
    logfire.configure(
        token=settings.LOGFIRE_TOKEN,
    )
else:
    logfire.configure(
        environment="local",
        local=True,
        send_to_logfire=False,
    )
logfire.instrument_fastapi(app)

app.add_exception_handler(AppError, app_exception_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user.router)
app.include_router(auth.router)
app.include_router(item.router)

admin = Admin(app, engine, authentication_backend=authentication_admin)
admin.add_view(AdminTable)


@app.get("/scalar", include_in_schema=False)
async def scalar_html():
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title=app.title,
        show_sidebar=True,
        hide_download_button=False,
        hide_models=False,
        dark_mode=True,
        search_hot_key=SearchHotKey.K,
        default_open_all_tags=True,
        # layout=Layout.CLASSIC,
        # servers=[
        #     {"url": "https://api.production.example.com"},
        #     {"url": "https://api.staging.example.com"},
        # ],
        # authentication={"bearerAuth": "your-static-token-if-needed"},
    )


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
