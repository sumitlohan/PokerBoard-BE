import os
from celery import Celery
from django.conf import settings
import class_settings

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'poker.settings.local')
os.environ.setdefault('DJANGO_SETTINGS_CLASS', 'Setting')
class_settings.setup()

app = Celery('poker')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(self.request)

