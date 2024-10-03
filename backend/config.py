from pydantic.networks import AnyHttpUrl
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "DhanHQ OHLC"

    API_PATH: str = "/api/v1"

    BACKEND_CORS_ORIGINS: list[AnyHttpUrl] = []

    ENVIRONMENT: str = ""

    DHANHQ_CLIENT_ID: str = ""

    DHANHQ_ACCESS_TOKEN: str = ""

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
