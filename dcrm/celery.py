# celery.py
from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dcrm.settings')

# create a Celery instance and configure it
celery_app = Celery('website')

# Load task modules from all registered Django app configs.
celery_app.config_from_object('django.conf:settings', namespace='CELERY')

# Auto-discover tasks in all installed apps
celery_app.autodiscover_tasks()

app.conf.update(
    result_expires=3600,
    worker_log_format='[%(asctime)s] [%(levelname)s] [%(task_name)s(%(task_id)s)] %(message)s',
    worker_redirect_stdouts_level='INFO',
    loglevel='info',  # Set the log level here
)