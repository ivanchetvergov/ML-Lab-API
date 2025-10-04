# app/worker/celery_app.py

import os
from celery import Celery

# --- 1 URL брокера (лежит в докере)
CELERY_BROKER_URL = os.environ.get("REDIS_URL", "redis://localhost:6379/0")

# --- 2 создаем экземпляр
celery_app = Celery(
    'ml_lab',
    broker=CELERY_BROKER_URL,
    backend=CELERY_BROKER_URL,
    include=['app.worker.tasks']
)

# --- 3 настройка
celery_app.conf.update(
    task_track_started=True,
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='Europe/Moscow', 
    enable_utc=True,
)

if __name__ == '__main__':
    celery_app.start()
