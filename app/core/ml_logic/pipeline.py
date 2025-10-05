# app/core/ml_logic/pipeline.py
import os
from datetime import datetime
from typing import Dict, Any, Callable

from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, f1_score
import joblib

from app.schemas.tasks_schemas import TaskResult

from app.core.ml_logic.data_loader import simulate_data_load
from app.core.ml_logic.model_factory import init_model

import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

MODEL_SAVE_PATH = "/tmp/models"
os.makedirs(MODEL_SAVE_PATH, exist_ok=True)

def full_training_pipeline(
    data_id: str,
    model_type: str,
    params: Dict[str, Any],
    validation_split: float,
    progress_callback: Callable[[float, str], None] = None
) -> TaskResult:
    """
    полный пайплайн обучения модели с возможностью передавать коллбэк прогресса.
    """
    def progress(p, msg):
        if progress_callback:
            progress_callback(p, msg)

    
    progress(0.0, "loading data")
    X, y = simulate_data_load(data_id)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=validation_split, random_state=42
    )

    progress(0.2, "initializing model")
    model = init_model(model_type, params)

    progress(0.5, "training model")
    model.fit(X_train, y_train)

    progress(0.8, "evaluating model")
    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred, average='binary')

    progress(0.9, "saving model")
    filename = f"{model_type}_{data_id}_{datetime.now().strftime('%Y%m%d%H%M%S')}.pkl"
    full_path = os.path.join(MODEL_SAVE_PATH, filename)
    joblib.dump(model, full_path)

    progress(1.0, "done")

    return {
        "accuracy": acc,
        "f1_score": f1,
        "model_type": model_type,
        "data_id": data_id,
        "trained_at": datetime.now(),
        "model_path": full_path
    }
