from fastapi import APIRouter

from .main_view import router as main_router

router = APIRouter(
    include_in_schema=False,
)
router.include_router(main_router)
