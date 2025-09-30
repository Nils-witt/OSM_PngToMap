from rest_framework import serializers
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']


class MessageSerializer(serializers.Serializer):
    message = serializers.CharField(max_length=1000)
    timestamp = serializers.DateTimeField()
    user = UserSerializer(read_only=True)