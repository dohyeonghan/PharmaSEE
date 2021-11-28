from django.shortcuts import render
from .models import Pill
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny
from .serializers import PillSerializer

class PillViewSet(ModelViewSet):
    queryset = Pill.objects.all()
    serializer_class = PillSerializer
    permission_classes = [AllowAny] #fixme : 인증적용


