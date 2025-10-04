# app/main.py

from fastapi import FastAPI
from app.api.endpoints import train, task

app = FastAPI(
    title="ML-Lab API:",
    description="API для асинхронного обучения и сравнения моделей машинного обучения.",
    version="0.1.0"
)

app.include_router(train.router, prefix="/api", tags=["Training"])
app.include_router(task.router, prefix="/api", tags=["Task Status"])

@app.get("/")
async def root():
    return {"message": "Welcome to ML-Lab API. Access /docs for Swagger UI."}