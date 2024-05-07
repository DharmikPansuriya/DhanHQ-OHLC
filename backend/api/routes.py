from backend.api.endpoints.health_checker import router as endpoint_health
from fastapi import APIRouter

router = APIRouter()
router.include_router(router=endpoint_health, prefix="/endpoint-health", tags=["Endpoint Health"])

@router.get("/health", tags=["Health"])
async def health():
    return {"status": "ok"}
