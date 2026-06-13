import os
from celery import Celery
from kombu import Queue, Exchange

# Standard Environment Variable Fetcher for independent worker nodes
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

celery_app = Celery(
    "monetlink_workers",
    broker=REDIS_URL,
    backend=REDIS_URL,
)

# Enterprise Task Routing & Worker Configuration
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="Asia/Kolkata",  # Strict alignment with India Standard Time for accurate daily resets
    enable_utc=True,
    task_track_started=True,
    worker_concurrency=8,     # Limits CPU threads per container to avoid starvation
    worker_prefetch_multiplier=1, # Forces workers to take exactly 1 task at a time (Fair distribution)
    
    # Priority Queuing: Clicks are high priority, Analytics are low priority
    task_queues=(
        Queue('high_priority_clicks', Exchange('high_priority_clicks'), routing_key='click.#'),
        Queue('low_priority_cron', Exchange('low_priority_cron'), routing_key='cron.#'),
    ),
    task_default_queue='high_priority_clicks',
    task_default_exchange='high_priority_clicks',
    task_default_routing_key='click.default',
)
