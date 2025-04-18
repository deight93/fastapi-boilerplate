from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class EnvSettings(BaseSettings):
    # 공통 설정
    ENV_STATE: str
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_MINUTES: int

    # 공통 admin 설정
    ADMIN_ID: str
    ADMIN_PASSWORD: str

    # 공통 Redis 설정
    REDIS_HOST: str
    REDIS_PORT: str
    REDIS_DATABASE: str

    # 공통 Postgresql 설정
    POSTGRES_HOST: str
    POSTGRES_PORT: str

    # prod, dev별 설정
    DEBUG: bool
    ALLOWED_ORIGINS: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    REDIS_PASSWORD: str

    model_config = SettingsConfigDict(extra="ignore", env_file_encoding="utf-8")

    @field_validator("ALLOWED_ORIGINS")
    def parsing_allowed_origins(cls, value):
        if isinstance(value, str):
            return [i.strip() for i in value.split(",")]
        return value


class GlobalSettings(BaseSettings):
    ENV_STATE: str

    model_config = SettingsConfigDict(
        env_file=".env", extra="allow", env_file_encoding="utf-8"
    )


class FactorySettings:
    @staticmethod
    def load():
        global_settings = GlobalSettings()
        env_state = global_settings.ENV_STATE

        if env_state not in ("dev", "prod"):
            raise ValueError("Invalid ENV_STATE value")

        prefix = f"{env_state}_"
        parsed_settings = {
            (key[len(prefix) :] if key.startswith(prefix) else key).upper(): value
            for key, value in global_settings.model_dump().items()
        }

        return EnvSettings(**parsed_settings)


settings = FactorySettings.load()
