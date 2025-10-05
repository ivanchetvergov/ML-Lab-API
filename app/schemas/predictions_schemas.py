from pydantic import BaseModel, Field
from typing import List, Union

# --- Запрос на предсказание
class PredictionRequest(BaseModel):
    # полный путь к модели
    model_path: str = Field(..., description="Full path to saved model")
    
    # [[feat1, feat2, ... , featn], ... , [feat1, feat2, ... , featn]]
    features: List[List[Union[int, float]]] = Field(
        ...,
        description="A list of samples for predict. Each sample must be a list of num features."
    )
    
    class Config:
        # пример для автодоки
        json_schema = {
            "example": {
                "model_path": "/tmp/model/LogisticReggresion_....pkl",
                "features": [
                    [0.1, 0.5, 2.3, 0.8],
                    [1.2, 0.4, 1.1, 0.9]
                ]
            }
        }
        
class PredictionResponse(BaseModel):
    predictions: List[Union[int, float]] = Field(
        ..., 
        description="List of predicted class labels or values."
    )
    model_path: str = Field(..., description="The model path used for prediction.")
    timestamp: str = Field(..., description="Time of prediction.")
    