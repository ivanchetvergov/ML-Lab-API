import joblib
import pandas as pd
from typing import List, Union
from datetime import datetime

from app.schemas.predictions_schemas import PredictionResponse

def make_prediction(model_path: str, 
                    features: List[List[Union[int, float]]]
                    ) -> PredictionResponse:
    """Загружает модель и делает предсказение

    Args:
        model_path (str): путь к модели
        features (List[List[Union[int, float]]]): фичи на основе которых будет сделано предсказание

    Returns:
        PredictionResponse: предсказание в виде pydantic схемы
    """
    # 1 --- загрузка данных ---- 
    try:
        model = joblib.load(model_path)
    except FileNotFoundError:
        raise FileNotFoundError(f"Model not found at path: {model_path}")
    
    # 2 --- подготовка данных ----
    data = pd.DataFrame(features)
    
    # 3 --- предсказание ---
    predictions = model.predict(data).tolist()
    
    # 4 --- формирование ответа ---
    return PredictionResponse(
        predictions=predictions,
        model_path=model_path,
        timestamp=datetime.now().isoformat()
    )