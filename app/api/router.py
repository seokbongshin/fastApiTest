from fastapi import APIRouter, Depends

from app.api.dependencies import get_current_token_payload
from app.api.v1.endpoints.calculator import router as calculator_router
from app.api.v1.endpoints.sample import router as sample_router

api_router = APIRouter(dependencies=[Depends(get_current_token_payload)])
api_router.include_router(calculator_router, prefix="/api/v1", tags=["calculator"])
api_router.include_router(sample_router, prefix="/api/v1", tags=["sample"])
