from rest_framework import serializers
from .models import Pill

class PillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pill
        fields = '__all__'

