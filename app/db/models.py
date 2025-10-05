# app/db/models.py
from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.orm import declarative_base
from datetime import datetime

Base = declarative_base()

class ModelResult(Base):
    __tablename__ = "model_results"
    
    # --- короткий ID для user'a
    id = Column(Integer, primary_key=True, index=True)
    
    # --- ID задачи Celery
    celery_task_id = Column(String, unique=True, index=True, nullable=False)
    
    # --- metadata
    model_type = Column(String, nullable=False)
    data_id = Column(String, nullable=False)
    
    # --- result
    accuracy = Column(Float, nullable=True)
    f1_score = Column(Float, nullable=True)
    
    # --- path
    trained_at = Column(DateTime, default=datetime.utcnow)
    
    # --- task status (PENDING, PROGRESS, SUCESS, FAILURE)
    status = Column(String, default="PENDING", nullable=False)
    