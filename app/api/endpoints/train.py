# app/api/endpoints/train.py

from fastapi import APIRouter, Request
from app.schemas.tasks_schemas import TrainRequest, TaskSubmitResponse
from app.worker.tasks import train_model_task

router = APIRouter(tags=["Training"])

@router.post("/train", response_model=TaskSubmitResponse, status_code=202)
async def run_training(request_body: TrainRequest, http_request: Request):
    """
    Submits a machine learning model training job to the Celery queue.
    """
    # --- 1 Launch asynchronous Celery task
    task = train_model_task.apply_async(
        kwargs=request_body.model_dump()
    )
    # --- 2 формируем ссылку
    display_id = task.id[:8] 
    status_path = f"/api/tsk/{display_id}"
    
    # --- 3 Return Task ID and status URL immediately (HTTP 202 Accepted)
    return TaskSubmitResponse(
        task_id=task.id,
        message="Training job submitted. Check status_url for results.",
        status_url=status_path
    )