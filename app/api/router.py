from fastapi import APIRouter

from app.api.v1.endpoints.sample import router as sample_router

api_router = APIRouter()
api_router.include_router(sample_router, prefix="/api/v1", tags=["sample"])
