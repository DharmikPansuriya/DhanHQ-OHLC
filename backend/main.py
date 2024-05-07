from api.routes import router
from config import settings
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from logging_config import config_logging

config_logging()


app = FastAPI(
    title="Server API",
    openapi_url=f"{settings.API_PATH}/openapi.json",
    docs_url=f"{settings.API_PATH}/docs",
    redoc_url=f"{settings.API_PATH}/redoc",
    openapi_version="3.0.0",
)

app.add_middleware(GZipMiddleware, minimum_size=1000)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router=router, prefix=settings.API_PATH)
