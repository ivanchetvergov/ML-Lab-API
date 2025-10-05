# app/api/endpoints/task.py

from fastapi import APIRouter
from celery.result import AsyncResult
from app.worker.celery_app import celery_app
from app.schemas.tasks_schemas import TaskStatusResponse, TaskResult
from datetime import datetime

router = APIRouter(tags=["Task Status"])
@router.get("/status/{task_id}", response_model=TaskStatusResponse, status_code=200)
def get_task_status(task_id: str):
    """Получает текущий статус, прогресс и результаты задачи Celery."""
    pass 
