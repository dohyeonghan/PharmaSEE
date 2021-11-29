from django.shortcuts import render
from .models import Pill,Reminder
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny
from .serializers import PillSerializer,ReminderSerializer

class PillViewSet(ModelViewSet):
    queryset = Pill.objects.all()
    serializer_class = PillSerializer
    permission_classes = [AllowAny] #fixme : 인증적용

class ReminderViewSet(ModelViewSet):
    queryset = Reminder.objects.all()
    serializer_class = ReminderSerializer
    permission_classes = [AllowAny]

