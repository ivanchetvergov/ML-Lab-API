-- Скрипт для инициализации таблиц Postgre

-- 1. таблица таск
CREATE TABLE tasks (
    -- ID для API
    id SERIAL PRIMARY KEY,

    -- полный ID для Celery
    celery_task_id VARCHAR(36) UNIQUE NOT NULL,

    -- метеданные 
    model_type VARCHAR(100) NOT NULL,
    data_id VARCHAR(100) NOT NULL,
    
    -- параметры обучения (JSONB лучше для неструктурированных данных)
    params_json JSONB, 
    
    -- статус и время
    submitted_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(50) NOT NULL DEFAULT 'PENDING',
    error_message TEXT NULL,
    
    -- ссылка на итоговую модель (будет NULL, пока задача не завершится успешно)
    final_model_id INTEGER NULL
);

-- 2. таблица для хранения только успешных моделей (Models Catalog)
CREATE TABLE models (
    -- ID модели который будет использоваться для Predict
    id SERIAL PRIMARY KEY,
    
    -- ссылка на исходную задачу 
    task_id INTEGER NOT NULL REFERENCES tasks(id) ON DELETE CASCADE,
    
    -- результаты
    accuracy DOUBLE PRECISION NOT NULL,
    f1_score DOUBLE PRECISION NOT NULL,
    
    -- путь к файлу модели
    model_path VARCHAR(255) UNIQUE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- добавляем внешний ключ из tasks в models
ALTER TABLE tasks
ADD CONSTRAINT fk_final_model
FOREIGN KEY (final_model_id) REFERENCES models(id) ON DELETE SET NULL;

-- индексы для быстрого поиска
CREATE INDEX idx_tasks_celery_id ON tasks (celery_task_id);
CREATE INDEX idx_models_task_id ON models (task_id);
