import logging
from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def main_health() :
    try:
        pass
    except Exception as e:
        logging.error(f"Main Health :{str(e)}")
        raise e
