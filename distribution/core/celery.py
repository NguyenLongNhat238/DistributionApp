import os
from celery import Celery
from celery.schedules import crontab
from django.conf import settings


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

# , broker="amqp://admin:admin@localhost:15672//"
app = Celery(
    "core", broker=f'amqp://distributions:distributions@172.16.1.27:5672')

app.config_from_object("django.conf:settings", namespace="CELERY")

# Celery Beat Settings

app.conf.beat_schedule = {

    "periodic_add_numbers": {

        "task": "user.tasks.add_numbers",
        "schedule": crontab(minute='*/15'),

    },
}

app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f"Request: {self.request!r}")
