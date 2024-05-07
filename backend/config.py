from pydantic.networks import AnyHttpUrl
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "X Service"

    API_PATH: str = "/api/v1"

    BACKEND_CORS_ORIGINS: list[AnyHttpUrl] = []

    ENVIRONMENT: str = ""

    AUTH_SERVER_URL: str = ""

    DB_DRIVER: str = "postgresql+psycopg"

    BASE_CONNECTION: str = ""

    BASE_CONNECTION_MARKET_SERVER: str = ""

    AUTH_SERVER_TOKEN: str = ""

    TRANSACTION_SERVER_URL: str = ""

    NEWS_BASE_URL: str = ""

    NEWS_API_KEY: str = ""

    NEWS_API_HOST: str = ""

    AWS_CENTRAL_REDIS_HOST: str = ""

    AWS_CENTRAL_REDIS_PORT: int = 6379

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
