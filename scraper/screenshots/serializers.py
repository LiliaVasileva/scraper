from rest_framework import serializers
from .models import Screenshot


class ScreenshotTaskSerializer(serializers.Serializer):
    start_url = serializers.URLField()
    num_links = serializers.IntegerField(min_value=1, max_value=10)


class ScreenshotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Screenshot
        fields = ['id', 'task', 'url', 'image', 'created_at']
