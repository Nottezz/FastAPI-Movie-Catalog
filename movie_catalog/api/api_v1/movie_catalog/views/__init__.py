__all__ = ("router",)
from .details_view import router as details_router
from .list_view import router

router.include_router(details_router)
