import os
from celery import Celery
from celery.schedules import crontab


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "a_core.settings")
app = Celery(
    "celery",
    broker_connection_retry=False,
    broker_connection_retry_on_startapp=True,
)
app.config_from_object("django.conf:settings")

app.autodiscover_tasks()
app.conf.beat_schedule = {
    "send_view_count_report": {
        "task": "a_website.tasks.send_view_count_report",
        "schedule": crontab(minute=0, hour=0, day_of_month='1'),
    }
}
