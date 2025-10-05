# app/core/ml_logic/model_factory.py
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC

from app.schemas.models_schemas import (
    LogisticRegressionParams,
    RandomForestParams,
    SVCParams
)

# реестр моделей, использующий Pydantic-схемы
MODEL_REGISTRY = {
    "LogisticRegression": {
        "class": LogisticRegression,
        "schema": LogisticRegressionParams
    },
    "RandomForestClassifier": {
        "class": RandomForestClassifier,
        "schema": RandomForestParams
    },
    "SVC": {
        "class": SVC,
        "schema": SVCParams
    }
}

def init_model(model_type: str, raw_params: dict):
    """
    Инициализирует модель по названию и параметрам.
    Использует Pydantic-схему для валидации и фильтрации параметров.
    """
    if model_type not in MODEL_REGISTRY:
        raise ValueError(f"unsupported model type: {model_type}")
    
    model_info = MODEL_REGISTRY[model_type]
    ModelClass = model_info['class']
    ParamsSchema = model_info['schema']
    
    # --- 1 валидация данных
    validated_params = ParamsSchema(**raw_params)

    # --- 2 преобразование в словарь
    filtered_params = validated_params.model_dump()
    
    # --- 3 инициализация и возврат
    return ModelClass(**filtered_params)