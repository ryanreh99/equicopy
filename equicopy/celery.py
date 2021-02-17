import os
from celery import Celery
from celery.schedules import crontab

from server.utils.redis import redis_api

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'equicopy.settings')

app = Celery('equicopy')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.broker_url = redis_api.get_broker_url()
app.conf.timezone = 'Asia/Kolkata'
app.conf.beat_schedule = {
    'update-every-day': {
        'task': 'equicopy.celery.update_redis_data',
        'schedule': crontab(hour=18, minute=0),
        'args': (),
    },
}

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

@app.task
def update_redis_data():
    os.system("python manage.py fetch_copy")
