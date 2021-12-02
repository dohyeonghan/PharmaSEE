import re

from django.conf import settings
from django.db import models
from django.urls import reverse

class TimestampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Pill(TimestampedModel):
    name = models.CharField(max_length=100)
    image_dir = models.ImageField(upload_to="pharmasee/pill/%Y/%m/%d")
    effect = models.CharField(max_length=500)
    side_effect = models.CharField(max_length=500)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["-id"]


class Reminder(TimestampedModel):
    title = models.CharField(max_length=100)
    user_id = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="reminders", on_delete=models.CASCADE
    )
    pill_id = models.ForeignKey(Pill, on_delete=models.CASCADE)
    dose = models.CharField(max_length=100)

    when_to_take = models.TimeField(auto_now=False)

    taken_time = models.TimeField(auto_now=False)
    is_taken_today = models.BooleanField(default=False)
    dose_taken_today = models.IntegerField(default=0)

    def __str__(self):
        return self.title #고민

    class Meta:
        ordering = ["-id"]

