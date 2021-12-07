from rest_framework import serializers
from .models import DnnImage

class DnnImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = DnnImage
        fields = '__all__'

