from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.mail import send_mail
from django.core.validators import RegexValidator
from django.db import models
from django.template.loader import render_to_string
from django.shortcuts import resolve_url

class User(AbstractUser):
    follower_set = models.ManyToManyField('self', blank = True)
    following_set = models.ManyToManyField('self', blank=True)

    # @property
    # def name(self):
    #     return f"{self.first_name} {self.last_name}".strip()

    def __str__(self):
        return self.username


