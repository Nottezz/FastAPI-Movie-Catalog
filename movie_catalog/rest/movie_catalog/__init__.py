from fastapi import APIRouter

from .list_view import router as list_router

router = APIRouter(prefix="/movie-catalog", tags=["movie-catalog"])
router.include_router(list_router)
