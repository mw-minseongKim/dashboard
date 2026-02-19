from fastapi import APIRouter

from dashboard.auth.views import router as auth_router
from dashboard.item.views import router as item_router

router = APIRouter(prefix="/api/v1")

router.include_router(auth_router)
router.include_router(item_router)
