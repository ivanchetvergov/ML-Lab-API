# app/api/endpoints/db.py
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text 
from app.db.database import get_db, engine, Base
from app.db.models import Task 

# 1. Создаем роутер
router = APIRouter(
    prefix="/db",
    tags=["Database Tools"]
)

# 2. Роутер для проверки подключения и наличия таблиц 
@router.get("/status")
def db_connection_status(db: Session = Depends(get_db)):
    """
    Проверяет:
    1. Подключение к БД (используя dependency injection).
    2. Наличие таблицы 'tasks'.
    """
    try:
        tasks_count = db.query(Task).count()
        
        return {
            "status": "success",
            "message": "PostgreSQL is connected and ORM models are mapped.",
            "data": {"tasks_count": tasks_count}
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail=f"DB Error: {e.__class__.__name__} - {e}"
        )

# 3. Ручка для пересоздания всех таблиц
@router.post("/recreate-tables", status_code=status.HTTP_201_CREATED)
def recreate_all_tables():
    """
    Удаляет и пересоздает все таблицы, определенные в Base.
    """
    try:        
        # Base.metadata содержит все наши модели
        Base.metadata.drop_all(bind=engine)
        Base.metadata.create_all(bind=engine)
        
        return {"message": "All tables dropped and recreated successfully."}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail=f"Failed to recreate tables: {e}"
        )

# 4. (Опционально) Тест сырого SQL-запроса
@router.get("/raw-test")
def raw_sql_test(db: Session = Depends(get_db)):
    """Выполняет простой сырой SQL-запрос для проверки соединения."""
    try:
        result = db.execute(text("SELECT 1 as is_connected")).scalar()
        
        if result == 1:
            return {"status": "success", "message": "Raw SQL query successful."}
        else:
            raise Exception("Raw SQL query failed to return 1.")
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail=f"Raw SQL test error: {e}"
        )