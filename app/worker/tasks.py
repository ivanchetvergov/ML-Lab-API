# app/worker/tasks.py 

from celery.utils.log import get_task_logger
from celery import current_task
from app.worker.celery_app import celery_app

# Импорт из новых модулей
from app.core.ml_logic.pipeline import full_training_pipeline 
from app.schemas.tasks_schemas import TaskResult 

logger = get_task_logger(__name__)

@celery_app.task(bind=True)
def train_model_task(self, data_id: str,
                     model_type: str, params: dict, 
                     validation_split: float
                     ):
    """
    Main Celery task: initiates the full ML training pipeline.
    """
    task_id = self.request.id
        
    # --- 1. define the progress callback function
    def progress_callback(progress_value: float, message: str):
        """Updates the Celery task state and meta info for status check endpoint."""
        final_progress = min(1.0, progress_value)
        # обновляем статус в Redis (для API)
        self.update_state(
            state='PROGRESS', 
            meta={'progress': final_progress, 'message': message}
        )
        log_message = (
        f"PROGRESS {int(progress_value*100):3}% | " 
        f"{message[:50]}"                          
        )

        logger.info(log_message)

    try:
        # initial status update
        progress_callback(0.0, "Starting full training pipeline.")

        # --- 2. Execute the centralized ML pipeline
        # NOTE: The pipeline returns a TaskResult object (Pydantic model)
        result_object: TaskResult = full_training_pipeline(
            data_id=data_id,
            model_type=model_type,
            params=params,
            validation_split=validation_split,
            progress_callback=progress_callback 
        )
        
        logger.info(f"TRAINING DONE | Accuracy={result_object.accuracy:.4f}")

        # --- 3. return a dictionary that Celery can serialize (Crucial fix!)
        return result_object.model_dump() 

    except Exception as e:
        error_message = f"Training failed: {type(e).__name__}: {str(e)}"
        logger.error(f"Task {task_id} FAILURE: {error_message}", exc_info=True)
        self.update_state(
            state='FAILURE',
            meta={
                'progress': 1.0,
                'message': error_message,
                'exc_type': type(e).__name__
            }
        )
        raise