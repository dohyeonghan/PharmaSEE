from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        user = User.objects.create(username=validated_data['username'])
        user.set_password(validated_data['password'])
        user.save()
        return user
        #user.password = validated_data['password'] -> 절대 바로 넣지 말기

    class Meta:
        model = User
        fields = ['pk', 'username', 'password']