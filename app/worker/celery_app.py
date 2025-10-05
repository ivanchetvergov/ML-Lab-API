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
        
    worker_log_format='%(asctime)s | %(levelname)s | %(processName)s | %(message)s',
    worker_task_log_format='%(asctime)s | %(levelname)s | Task: %(task_id).8s | %(message)s', 
    worker_task_success_log_format='%(asctime)s | SUCCESS | Task: %(task_id).8s | took %(task_duration).4fs',
    worker_task_failure_log_format='%(asctime)s | FAILURE | Task: %(task_id).8s | %(exc)s',
    
    enable_utc=True
)

if __name__ == '__main__':
    celery_app.start()
