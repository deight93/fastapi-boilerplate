from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from redis import Redis
from sqladmin import Admin
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.admin.auth import authentication_admin
from app.admin.views import UserAdmin
from app.core.database import engine
from app.core.dependency import get_db, get_redis
from app.core.metadata import swagger_metadata
from app.core.setting import settings
from app.routers import auth, user


@asynccontextmanager
async def lifespan(app: FastAPI):
    print(f"INFO:     Hello, Run the server in the {settings.APP_ENV} environment 👋")
    yield
    print(
        f"INFO:     Bye, Shut down the server in the {settings.APP_ENV} environment 👋"
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
def file_logging_test():
    from app.core.logger import logging

    logger = logging.getLogger(__name__)
    logger.info("logging test ...")

    return {"logging_check": "logging success"}


@app.get("/api-health-check")
def api_health_check():
    from app.core.logger import logging

    logger = logging.getLogger(__name__)
    logger.error("Redis client is not initialized.")

    return {
        "api_health_check": "api-server is Ok",
        "debug-mode": settings.DEBUG,
    }


@app.get("/postgresql-health-check")
async def postgresql_health_check(db: Session = Depends(get_db)):
    try:
        value = db.execute(select(1)).scalar()
        if value == 1:
            return {"postgresql_health_check": "postgresql-server is Ok"}
        else:
            return {
                "postgresql_health_check": "postgresql-server is not responding correctly"
            }
    except Exception as e:
        return {"postgresql_health_check": f"postgresql-server error: {str(e)}"}


@app.get("/redis-health-check")
def redis_health_check(redis: Redis = Depends(get_redis)):
    redis.set("redis_health_check", "Ok")
    value = redis.get("redis_health_check")
    return {"redis_health_check": f"redis-server is {value}"}


app.mount("/static", StaticFiles(directory="app/core/static"), name="static")
