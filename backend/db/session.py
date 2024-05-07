import json
import logging
from collections.abc import Generator
from contextvars import ContextVar
from urllib.parse import urljoin

from api.utils import get_cache_key_for_db_engine
from cachetools import TTLCache
from config import settings
from fastapi import HTTPException, Request
from requests.adapters import HTTPAdapter
from requests.sessions import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from starlette.status import HTTP_401_UNAUTHORIZED

session_var = ContextVar("session", default=None)

session = Session()

# Customize the adapter with a larger pool size
adapter = HTTPAdapter(pool_connections=100, pool_maxsize=100)

# Mount the adapter to your session
session.mount(settings.AUTH_SERVER_URL, adapter)

cache = TTLCache(maxsize=200, ttl=5 * 60)

REDIS_ONE_HOUR_TIME = 60 * 60


def fetch_client_creds_from_token(token: str) -> dict | None:
    # Check if environment is production
    if settings.ENVIRONMENT == "production":
        from utils.redis_utils import RedisClient

        redis = RedisClient.get_instance()
        response = redis.get(token)
        if response:
            response = json.loads(response.decode("utf-8"))
            return response

    # If no cache hit or not in production, fetch from auth server
    auth_url = urljoin(settings.AUTH_SERVER_URL, "/api/middlewaredata")
    try:
        response = session.get(auth_url, headers={"Authorization": token})
        response.raise_for_status()
        response = response.json()

        # If in production, cache the response
        if settings.ENVIRONMENT == "production":
            redis.setex(token, REDIS_ONE_HOUR_TIME, json.dumps(response).encode("utf-8"))

        return response
    except Exception as e:
        logging.error(f"Error fetching client credentials: {e}")
        return None


def create_db_engine(user, password, host, port, name):
    try:
        cache_key = get_cache_key_for_db_engine(user, password, host, port, name)
        cached_result = cache.get(cache_key)

        if cached_result is not None:
            return cached_result

        engine = create_engine(
            f"{settings.DB_DRIVER}://{user}:{password}@{host}:{port}/{name}", pool_size=10, max_overflow=20
        )
        cache[cache_key] = engine
        return engine
    except Exception as e:
        logging.error(f"error in create db engine : {e}")
        return None


def get_db(request: Request) -> Generator[tuple[Session, list[dict], dict], None, None]:
    token = request.headers.get("Authorization")
    user_credentials = fetch_client_creds_from_token(token)

    if not user_credentials:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    credentials = user_credentials.get("credential", {})

    user = credentials.get("db_user")
    host = credentials.get("db_host")
    port = credentials.get("db_port")
    password = credentials.get("db_pass")
    name = credentials.get("db_name")

    engine = create_db_engine(user, password, host, port, name)

    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    session = SessionLocal()
    session_var.set(session)

    clients = user_credentials.get("clients", [])
    user = user_credentials.get("user", {})
    s3 = {
        "access_key": credentials.get("s3_access_key"),
        "secret_key": credentials.get("s3_secret_key"),
        "bucket_name": credentials.get("s3_bucket"),
        "region_name": credentials.get("s3_region"),
    }

    kwargs = {"token": token, "s3": s3}

    try:
        yield session, clients, user, kwargs
    finally:
        session.close()
