from rest_framework import serializers
from .models import Pill,Reminder
from django.contrib.auth import get_user_model


class PillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pill
        fields = '__all__'

class ReminderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reminder
        fields = '__all__'