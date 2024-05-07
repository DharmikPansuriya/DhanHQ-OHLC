from collections.abc import Generator
from contextvars import ContextVar

import requests
from config import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

session_var = ContextVar("session", default=None)

session = requests.Session()


def get_market_db() -> Generator[Session, None, None]:
    engine = create_engine(f"{settings.BASE_CONNECTION_MARKET_SERVER}")

    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    session = SessionLocal()
    session_var.set(session)

    try:
        yield session
    except Exception as e:
        print("Error in get Market DB", e)
        session.rollback()
        raise
    finally:
        session.close()
