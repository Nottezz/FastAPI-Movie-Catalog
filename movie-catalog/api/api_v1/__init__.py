from fastapi import APIRouter

from .movie_catalog.views import router as movie_catalog_router

router = APIRouter(
    prefix="/v1",
)
router.include_router(movie_catalog_router)
