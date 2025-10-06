# app/db/models.py
from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text, JSON
from sqlalchemy.orm import relationship

from app.db.database import Base 

class Task(Base):
    """
    Модель для таблицы 'tasks'. 
    Отслеживает все запущенные задачи обучения (PENDING, SUCCESS, FAILURE).
    """
    __tablename__ = "tasks"

    # Основной ID задачи для внешнего API
    id = Column(Integer, primary_key=True, index=True) 
    
    # Полный UUID задачи Celery для внутреннего мониторинга
    celery_task_id = Column(String(36), unique=True, index=True, nullable=False)
    
    # Метаданные запроса
    model_type = Column(String, nullable=False)
    data_id = Column(String, nullable=False)
    params_json = Column(JSON, default={}) # спользуем тип JSONB в PostgreSQL
    
    # Статус и время
    submitted_at = Column(DateTime, default=datetime.utcnow)
    status = Column(String, default="PENDING", nullable=False) 
    error_message = Column(Text, nullable=True)
    
    # Внешний ключ
    final_model_id = Column(Integer, ForeignKey("models.id"), nullable=True)

    # Relationship: Позволяет обращаться к модели как к атрибуту (task.result_model)
    result_model = relationship("Model", back_populates="source_task", foreign_keys=[final_model_id])


class Model(Base):
    """
    Модель для таблицы 'models'. 
    Каталог только для успешно обученных моделей, готовых к использованию.
    """
    __tablename__ = "models"

    # ID модели для Predict API
    id = Column(Integer, primary_key=True, index=True)
    
    # Внешний ключ, который ссылается на исходную задачу
    task_id = Column(Integer, ForeignKey("tasks.id"), unique=True, nullable=False)
    
    # Результаты
    accuracy = Column(Float, nullable=False)
    f1_score = Column(Float, nullable=False)
    
    # Путь к сохраненному файлу
    model_path = Column(String(255), unique=True, nullable=False)
    trained_at = Column(DateTime, default=datetime.utcnow)

    # Relationship: Позволяет обращаться к задаче как к атрибуту (model.source_task)
    source_task = relationship("Task", back_populates="result_model", foreign_keys=[task_id])