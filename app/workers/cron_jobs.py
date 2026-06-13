from celery.schedules import crontab
from .celery_app import celery_app

# ==============================================================================
# ENTERPRISE SCHEDULER: CELERY BEAT CRON MATRIX
# ==============================================================================

celery_app.conf.beat_schedule = {
    # 1. Hourly Deep Fraud Sweep (Runs every hour at minute 0)
    "hourly_fraud_sweep": {
        "task": "workers.sweep_fraudulent_clicks_task",
        "schedule": crontab(minute=0),
        "options": {"queue": "low_priority_cron"}
    },
    
    # 2. Daily Metrics Aggregation (Runs every midnight IST - 00:01)
    "daily_analytics_aggregator": {
        # Assuming we have an aggregation task mapped
        "task": "workers.aggregate_daily_metrics_task", 
        "schedule": crontab(hour=0, minute=1),
        "options": {"queue": "low_priority_cron"}
    },
    
    # 3. Weekly Database Vacuum/Optimization (Runs every Sunday at 3 AM)
    "weekly_db_optimization": {
        "task": "workers.vacuum_database_task",
        "schedule": crontab(day_of_week='sun', hour=3, minute=0),
        "options": {"queue": "low_priority_cron"}
    }
}
