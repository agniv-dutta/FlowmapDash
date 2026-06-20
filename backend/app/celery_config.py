import os
from celery import Celery

# Configure Celery with Redis as broker
celery = Celery(
    'flowmapdash',
    broker=os.getenv('REDIS_URL', 'redis://localhost:6379/0'),
    backend=os.getenv('REDIS_URL', 'redis://localhost:6379/0'),
    include=['app.tasks']
)

# Celery configuration
celery.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
    task_track_started=True,
    task_time_limit=30 * 60,  # 30 minutes
    task_soft_time_limit=25 * 60,  # 25 minutes
    worker_prefetch_multiplier=4,
    worker_max_tasks_per_child=1000,
)

# Optional: Configure task routes
celery.conf.task_routes = {
    'app.tasks.process_batch_events': {'queue': 'heavy'},
    'app.tasks.generate_analytics': {'queue': 'analytics'},
}
