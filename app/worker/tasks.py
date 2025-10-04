# app/worker/tasks.py

from celery.utils.log import get_task_logger
from datetime import datetime
from celery import current_task
from sklearn.linear_model import LogisticRegression # type: ignore
from app.schemas.schemas import TaskResult 
from app.worker.celery_app import celery_app

import numpy as np
import joblib 
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, f1_score

logger = get_task_logger(__name__)

MODEL_SAVE_PATH = "/tmp/models" 

def simulate_data_load(data_id: str):
    """Simulate loading data based on data_id and return synthetic data."""

    X = np.random.rand(100, 5) 
    y = (X.sum(axis=1) > 2.5).astype(int) 
    
    return X, y

@celery_app.task(bind=True)
def train_model_task(self, data_id: str, model_type: str, params: dict, validation_split: float) -> TaskResult:
    """
    Main Celery task to train an ML model asynchronously.
    """
    task_id = self.request.id
    logger.info(f"Starting training for Task ID: {task_id}")
    self.update_state(state='STARTED', meta={'progress': 0.0, 'message': 'Task initialized.'})

    try:
        # --- 1  data loading and split
        self.update_state(state='PROGRESS', meta={'progress': 0.1, 'message': 'Loading and splitting data...'})
        X, y = simulate_data_load(data_id)
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=validation_split, random_state=42)
        
        # --- 2 model init
        self.update_state(state='PROGRESS', meta={'progress': 0.2, 'message': f'Initializing model: {model_type}'})
        
        if model_type == "LogisticRegression":
            model = LogisticRegression(**params)
        else:
            raise ValueError(f"Unsupported model type: {model_type}")

        # --- 3 train
        self.update_state(state='PROGRESS', meta={'progress': 0.5, 'message': 'Model training in progress...'})
        model.fit(X_train, y_train) 

        # --- 4 evaluation
        self.update_state(state='PROGRESS', meta={'progress': 0.8, 'message': 'Evaluating model performance...'})
        y_pred = model.predict(X_test)
        
        final_accuracy = accuracy_score(y_test, y_pred)
        final_f1 = f1_score(y_test, y_pred, average='binary') # Assuming binary classification
        
        # --- 5 saving model
        model_filename = f"{model_type}_{data_id}_{task_id}.pkl"
        full_path = f"{MODEL_SAVE_PATH}/{model_filename}"
        joblib.dump(model, full_path)
        logger.info(f"Model saved to: {full_path}")
        
        # --- 6 metrics
        final_metrics = {
            "accuracy": final_accuracy, 
            "f1_score": final_f1, 
            "model_type": model_type,
            "data_id": data_id,
            "trained_at": datetime.now(),
            "model_path": full_path 
        }
        
        result_object = TaskResult(**final_metrics)
        return result_object.model_dump()

    except Exception as e:
        error_message = f"Training failed: {type(e).__name__}: {str(e)}"
        logger.error(error_message, exc_info=True)
        self.update_state(state='FAILURE', meta={'message': error_message})
        raise