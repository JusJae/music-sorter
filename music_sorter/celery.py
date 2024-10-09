from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'music_sorter.settings')

app = Celery('music_sorter')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
