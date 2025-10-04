# app/api/endpoints/train.py

from fastapi import APIRouter, Request
from app.schemas.schemas import TrainRequest, TaskSubmitResponse
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
    
    # Construct the full status URL using the current request URL base
    base_url = str(http_request.base_url).rstrip('/')
    status_url = f"{base_url}/task/{task.id}" 
    
    # --- 2 Return Task ID and status URL immediately (HTTP 202 Accepted)
    return TaskSubmitResponse(
        task_id=task.id,
        message="Training job submitted. Check status_url for results.",
        status_url=status_url
    )