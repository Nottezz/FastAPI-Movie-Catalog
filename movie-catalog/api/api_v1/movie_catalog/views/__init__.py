from .list_view import router
from .details_view import router as details_router

router.include_router(details_router)
