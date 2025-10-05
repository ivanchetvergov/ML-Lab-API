# app/api/endpoints/predict.py

from fastapi import APIRouter, Request
from app.schemas.predictions_schemas import PredictionRequest, PredictionResponse
from app.core.ml_logic.predictor import make_prediction

router = APIRouter(tags=["Predict"])

@router.post("/predict", response_model=PredictionResponse, status_code=202)
async def predict_endpoint(request: PredictionRequest) -> PredictionResponse:
    """Выполняет синхронное предсказание с исп. сохраненной модели

    Args:
        request (PredictionRequest): запрос в виде pydantic схемы

    Returns:
        PredictionResponse: ответ в виде pydantic схемы
    """
    try:
        response = make_prediction(
            model_path=request.model_path,
            features=request.features
        )
        return response
    except FileNotFoundError as e:
        raise RuntimeError(f"predict endpoint failure: {e}")
    