from api.endpoints.health_checker import router as endpoint_health
from api.endpoints.main import router as dhanhq_ohlc_router
from fastapi import APIRouter

router = APIRouter()
router.include_router(router=endpoint_health,
                      prefix="/endpoint-health", tags=["Endpoint Health"])
router.include_router(router=dhanhq_ohlc_router,
                      prefix="/dhanhq", tags=["Dhan HQ"])


@router.get("/health", tags=["Health"])
async def health():
    return {"status": "ok"}
