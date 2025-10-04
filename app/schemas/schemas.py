# app/schemas/schemas.py

from pydantic import BaseModel, Field
from typing import Dict, Any, Optional
from datetime import datetime


class TrainRequest(BaseModel):
    '''
    pydantic schema for request that starts model training
    '''
    data_id: str = Field(..., description="unique id of the loaded dataset")
    model_type: str = Field(..., description="type of ml model (e.g., RandomForest, XGBoost, etc.)")
    params: Dict[str, Any] = Field(default_factory=dict, description="dictionary with model hyperparameters")
    validation_split: float = Field(default=0.2, description="train/test data split ratio")


class TaskSubmitResponse(BaseModel):
    '''
    pydantic schema for response after submitting training task
    '''
    task_id: str = Field(..., description="unique celery task id")
    message: str = Field(..., description="short status message")
    status_url: str = Field(..., description="endpoint to check current task status")


class TaskResult(BaseModel):
    '''
    pydantic schema for ml training result (metrics and meta info)
    '''
    accuracy: float = Field(..., description="model accuracy score on validation set")
    f1_score: float = Field(..., description="model f1 score on validation set")
    model_type: str = Field(..., description="model type that was trained")
    data_id: str = Field(..., description="dataset id used for training")
    trained_at: datetime = Field(default_factory=datetime.now, description="timestamp when training finished")


class TaskStatusResponse(BaseModel):
    '''
    pydantic schema for checking task status and progress
    '''
    task_id: str = Field(..., description="unique celery task id")
    status: str = Field(..., description="current task status (PENDING, STARTED, SUCCESS, FAILURE, etc.)")
    message: Optional[str] = Field(None, description="optional status or error message")
    progress: Optional[float] = Field(None, description="training progress percentage (0.0 - 1.0)")
    result: Optional[TaskResult] = Field(None, description="training result if task completed")
    timestamp: datetime = Field(default_factory=datetime.now, description="current server timestamp for response")
