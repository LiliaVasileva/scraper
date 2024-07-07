import os
import uuid
from django.conf import settings
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import ScreenshotTask, Screenshot
from .serializers import ScreenshotTaskSerializer, ScreenshotSerializer
from .tasks import capture_screenshots
from django.http import HttpResponse
import time

class IsAliveView(APIView):
    def get(self, request):
        return Response({"status": "alive"}, status=status.HTTP_200_OK)

class ScreenshotCreateView(APIView):
    def post(self, request):
        start_url = request.data.get('start_url')
        num_links = int(request.data.get('num_links'))

        if not start_url or not num_links:
            return Response({"error": "Missing required parameters"}, status=status.HTTP_400_BAD_REQUEST)

        task_id = str(uuid.uuid4())
        task = ScreenshotTask.objects.create(task_id=task_id)

        capture_screenshots.delay(task_id, start_url, num_links)

        return Response({"task_id": task_id}, status=status.HTTP_202_ACCEPTED)

class ScreenshotListView(APIView):
    def get(self, request, task_id):
        task = get_object_or_404(ScreenshotTask, task_id=task_id)
        screenshots = task.screenshots.all()
        serializer = ScreenshotSerializer(screenshots, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

