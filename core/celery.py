import datetime
import os

from celery import Celery
from celery.schedules import crontab
from django.utils import timezone

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

app = Celery("worker", broker="amqp://admin:admin@localhost:5672")

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object("django.conf:settings", namespace="CELERY")

# Load task modules from all registered Django apps.
app.autodiscover_tasks()

app.conf.beat_schedule = {
    "add-every-1-odd-hour": {
        "task": "celery_beat.tasks.add_five_quotes",
        "schedule": crontab(minute=0, hour="1-23/2"),
    }
}
