from pydantic import PostgresDsn, RedisDsn, computed_field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class EnvSettings(BaseSettings):
    model_config = SettingsConfigDict(extra="ignore", env_file_encoding="utf-8")

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
    REDIS_PORT: int
    REDIS_DATABASE: str

    # 공통 Postgresql 설정
    POSTGRES_HOST: str
    POSTGRES_PORT: int

    # prod, dev별 설정
    DEBUG: bool
    ALLOWED_ORIGINS: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    REDIS_PASSWORD: str

    @field_validator("ALLOWED_ORIGINS")
    def parsing_allowed_origins(cls, value):  # noqa: N805
        if isinstance(value, str):
            return [i.strip() for i in value.split(",")]
        return value

    @computed_field
    @property
    def redis_url(self) -> RedisDsn:
        """
        This is a computed field that generates a RedisDsn URL for redis-py.

        The URL is built using the MultiHostUrl.build method, which takes the following parameters:
        - scheme: The scheme of the URL. In this case, it is "redis".
        - host: The host of the Redis database, retrieved from the REDIS_HOST environment variable.
        - port: The port of the Redis database, retrieved from the REDIS_PORT environment variable.
        - path: The path of the Redis database, retrieved from the REDIS_DB environment variable.

        Returns:
            RedisDsn: The constructed RedisDsn URL for redis-py.
        """
        return RedisDsn.build(
            scheme="redis",
            password=self.REDIS_PASSWORD,
            host=self.REDIS_HOST,
            port=self.REDIS_PORT,
            path=self.REDIS_DATABASE,
        )

    @computed_field
    @property
    def asyncpg_url(self) -> PostgresDsn:
        """
        This is a computed field that generates a PostgresDsn URL for asyncpg.

        The URL is built using the MultiHostUrl.build method, which takes the following parameters:
        - scheme: The scheme of the URL. In this case, it is "postgresql+asyncpg".
        - username: The username for the Postgres database, retrieved from the POSTGRES_USER environment variable.
        - password: The password for the Postgres database, retrieved from the POSTGRES_PASSWORD environment variable.
        - host: The host of the Postgres database, retrieved from the POSTGRES_HOST environment variable.
        - path: The path of the Postgres database, retrieved from the POSTGRES_DB environment variable.

        Returns:
            PostgresDsn: The constructed PostgresDsn URL for asyncpg.
        """
        return PostgresDsn.build(
            scheme="postgresql+asyncpg",
            username=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
            host=self.POSTGRES_HOST,
            port=self.POSTGRES_PORT,
            path=self.POSTGRES_DB,
        )

    @computed_field
    @property
    def postgres_url(self) -> PostgresDsn:
        """
        This is a computed field that generates a PostgresDsn URL

        The URL is built using the MultiHostUrl.build method, which takes the following parameters:
        - scheme: The scheme of the URL. In this case, it is "postgres".
        - username: The username for the Postgres database, retrieved from the POSTGRES_USER environment variable.
        - password: The password for the Postgres database, retrieved from the POSTGRES_PASSWORD environment variable.
        - host: The host of the Postgres database, retrieved from the POSTGRES_HOST environment variable.
        - path: The path of the Postgres database, retrieved from the POSTGRES_DB environment variable.

        Returns:
            PostgresDsn: The constructed PostgresDsn URL.
        """
        return PostgresDsn.build(
            scheme="postgresql",
            username=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
            host=self.POSTGRES_HOST,
            path=self.POSTGRES_DB,
        )


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
