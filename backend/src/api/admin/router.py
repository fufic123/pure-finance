from fastapi import APIRouter, Depends

from src.api.admin.dependencies import require_admin
from src.api.admin.routers import logs, models, stats, tasks, users

router = APIRouter(
    prefix="/admin",
    dependencies=[Depends(require_admin)],
)

router.include_router(users.router)
router.include_router(models.router)
router.include_router(tasks.router)
router.include_router(stats.router)
router.include_router(logs.router)
