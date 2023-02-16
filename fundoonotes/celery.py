from __future__ import absolute_import,unicode_literals
import os
from celery import Celery
from django.conf import settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE','fundoonotes.settings')
app= Celery('fundoonotes')
app.conf.enable_utc=False
app.conf.update(timezone='Asia/Kolkata')
app.config_from_object(settings,namespace='CELERY')
app.conf.beat_schedule={
    # 'send-mail-every-day-8':{
    #     'task':'send_mail_app.tasks.send_mail_func',
    #     'schedule':crontab(hour=17,minute=7),
    #      # 'args':(2)
    }


app.autodiscover_tasks()
@app.task(bind=True)
def debug_task(self):
    print(f'Request:{self.request!r}')
