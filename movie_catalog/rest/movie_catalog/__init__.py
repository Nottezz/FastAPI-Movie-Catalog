from dependencies.auth import user_basic_auth_required_for_unsafe_methods
from fastapi import APIRouter, Depends

from .create_view import router as create_router
from .list_view import router as list_router
from .update_view import router as update_router

router = APIRouter(
    prefix="/movie-catalog",
    tags=["movie-catalog"],
    dependencies=[
        Depends(user_basic_auth_required_for_unsafe_methods),
    ],
)
router.include_router(list_router)
router.include_router(create_router)
router.include_router(update_router)
