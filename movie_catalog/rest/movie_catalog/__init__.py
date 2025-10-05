from fastapi import APIRouter

from .create_view import router as create_router
from .list_view import router as list_router

router = APIRouter(prefix="/movie-catalog", tags=["movie-catalog"])
router.include_router(list_router)
router.include_router(create_router)
