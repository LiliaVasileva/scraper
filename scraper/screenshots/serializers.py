from rest_framework import serializers
from .models import Screenshot, ScreenshotTask


class ScreenshotTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScreenshotTask
        fields = ['id', 'task_id', 'created_at']


class ScreenshotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Screenshot
        fields = ['id', 'task', 'url', 'image', 'created_at']
