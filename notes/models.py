import datetime
import json
from datetime import datetime
from datetime import timedelta

from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django_celery_beat.models import CrontabSchedule, PeriodicTask

from user.models import User


# Create your models here.
class Labels(models.Model):
    label_name = models.CharField(max_length=150, unique=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.label_name)


class Note(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    collaborator = models.ManyToManyField(User, related_name='collaborator')
    label = models.ManyToManyField(Labels)
    isArchive = models.BooleanField(default=False)
    isTrash = models.BooleanField(default=False)
    color = models.CharField(max_length=10, null=True, blank=True)
    reminder = models.DateTimeField(null=True, blank=True)
    image = models.ImageField(upload_to='images/', null=True, blank=True)

    def __str__(self):
        return str(self.title)

    class Meta:
        verbose_name = "Note"


@receiver(post_save, sender=Note)
def reminder_handler(sender, instance, **kwargs):
    if instance.reminder:
        current_date = datetime.now()
        reminder_date = instance.reminder.date()
        no_of_days = (reminder_date - current_date.date()).days
        reminder_time = datetime.now() + timedelta(days=no_of_days)
        schedule_task(instance, reminder_time)


def schedule_task(instance, reminder_time):
    schedule, created = CrontabSchedule.objects.get_or_create(
        hour=instance.reminder.hour,
        minute=instance.reminder.minute,
        day_of_month=reminder_time.day,
        month_of_year=instance.reminder.month
    )
    existing_task = PeriodicTask.objects.filter(name=f"Task for note {instance.id}").first()
    if existing_task is not None:
        existing_task.crontab = schedule
        existing_task.save()
    else:
        new_task = PeriodicTask.objects.create(
            crontab=schedule,
            name=f"Task for note{instance.id}",
            task='notes.tasks.send_mail_func',
            args=json.dumps([
                instance.title,
                instance.description,
                [instance.user.email]

            ]))
