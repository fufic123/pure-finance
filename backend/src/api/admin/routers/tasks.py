from fastapi import APIRouter
from fastapi.responses import JSONResponse

router = APIRouter(prefix="/tasks", tags=["admin-tasks"])

_KNOWN_TASKS = {"take_daily_snapshots": "tasks.take_daily_snapshots"}


@router.get("")
async def list_tasks() -> list[str]:
    return list(_KNOWN_TASKS.keys())


@router.post("/{task_name}/run", status_code=202)
async def run_task(task_name: str) -> dict:
    celery_name = _KNOWN_TASKS.get(task_name)
    if celery_name is None:
        return JSONResponse(status_code=404, content={"message": f"task '{task_name}' not found"})
    from src.workers.celery_app import celery_app
    result = celery_app.send_task(celery_name)
    return {"task_id": result.id, "task_name": task_name, "status": "queued"}
