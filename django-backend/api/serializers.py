from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Project  # Assuming a Project model exists

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']


class MessageSerializer(serializers.Serializer):
    message = serializers.CharField(max_length=1000)
    timestamp = serializers.DateTimeField()
    user = UserSerializer(read_only=True)

class ProjectSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Project
        read_only_fields = ['status', 'created_at', 'updated_at','owner']
        fields = ['url','id', 'name', 'description','min_zoom','max_zoom', 'coordinates','status','owner', 'created_at', 'updated_at']

    def create(self, validated_data):
        instance = super().create(validated_data)
        instance.owner = self.context['request'].user
        instance.save()
        return instance
