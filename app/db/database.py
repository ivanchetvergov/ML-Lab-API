# app/db/database.py
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from typing import Generator

# 1. Получение URL базы данных
SQLALCHEMY_DATABASE_URL = os.environ.get("DATABASE_URL")

if not SQLALCHEMY_DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is not set. Check your .env or docker-compose.yml.")

# 2. Создание движка (Engine)
# Engine - это интерфейс, который соединяет SQLAlchemy с базой данных.
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_pre_ping=True
)

# 3. Создание базового класса для ORM-моделей
Base = declarative_base()

# 4. Создание фабрики сессий (SessionLocal)
SessionLocal = sessionmaker(
    autocommit=False, 
    autoflush=False, 
    bind=engine
)

# 5. Функция-зависимость для FastAPI
def get_db() -> Generator:
    """
    Предоставляет сессию базы данных для запроса и гарантирует 
    ее закрытие после завершения или ошибки.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()