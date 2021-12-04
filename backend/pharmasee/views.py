from django.shortcuts import render
from .models import Pill,Reminder
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny, DjangoObjectPermissions
from .serializers import PillSerializer,ReminderSerializer
from django.db.models import Q
import django_filters.rest_framework
from rest_framework import generics, filters

class PillViewSet(ModelViewSet):
    queryset = Pill.objects.all()
    serializer_class = PillSerializer
    permission_classes = [AllowAny] #fixme : 인증적용

class ReminderViewSet(ModelViewSet):
    queryset = Reminder.objects.all()
    # qeuryset = Reminder.objects.filter(user_id=2)
    serializer_class = ReminderSerializer
    permission_classes = [AllowAny]

class PillListView(generics.ListAPIView):
    queryset = Pill.objects.all()
    serializer_class = PillSerializer
    # filter_backends = [filters.SearchFilter]
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_fields = ['name', 'effect']
    search_fields = ['name','effect']
