# app/api/endpoints/task.py

from fastapi import APIRouter
from celery.result import AsyncResult
from app.worker.celery_app import celery_app
from app.schemas.schemas import TaskStatusResponse, TaskResult
from datetime import datetime

router = APIRouter(tags=["Task Status"])

def _build_response(task: AsyncResult, status: str, message: str, progress: float | None = None, result: TaskResult | None = None) -> TaskStatusResponse:
    """
    Helper function to construct the TaskStatusResponse object.
    """
    return TaskStatusResponse(
        task_id=task.id,
        status=status,
        message=message,
        progress=progress,
        result=result,
        timestamp=datetime.now()
    )

@router.get("/task/{task_id}", response_model=TaskStatusResponse)
async def get_task_status(task_id: str) -> TaskStatusResponse:
    """
    Fetches the current status and result of a Celery task by ID.
    """
    task = AsyncResult(task_id, app=celery_app)
    # safely access task metadata, defaulting to an empty dict
    info = task.info if isinstance(task.info, dict) else {}

    # --- 1 Task is running, waiting, or retrying ---
    if task.state in {"PENDING", "STARTED", "PROGRESS", "RETRY"}:
        default_message = f"Task is currently in state: {task.state}"
        
        return _build_response(
            task,
            task.state,
            info.get("message", default_message),
            progress=info.get("progress")
        )

    # --- 2 Task completed successfully ---
    if task.state == "SUCCESS":
        try:
            result = TaskResult(**task.result)
        except Exception as e:
            return _build_response(task, "ERROR", f"Result parsing failed: {e}", progress=1.0)
            
        return _build_response(task, "COMPLETED", "Training finished successfully.", progress=1.0, result=result)

    # --- 3 Task failed or was revoked ---
    if task.state in {"FAILURE", "REVOKED"}:
        error_message = info.get("message", f"Task failed with state: {task.state}")
        
        return _build_response(task, task.state, error_message, progress=1.0)

    # --- 4 Unknown/Unhandled State ---
    return _build_response(task, "UNKNOWN", f"Task is in an unhandled state: {task.state}")