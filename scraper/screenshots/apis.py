import uuid
from drf_yasg.utils import swagger_auto_schema
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import ScreenshotTask
from .serializers import ScreenshotTaskSerializer, ScreenshotSerializer
from .tasks import capture_screenshots


class IsAliveView(APIView):
    def get(self, request):
        return Response({"status": "alive"}, status=status.HTTP_200_OK)


class ScreenshotsAPIView(APIView):
    serializer_class = ScreenshotTaskSerializer

    @swagger_auto_schema(
        request_body=ScreenshotTaskSerializer,
    )
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            start_url = serializer.validated_data['start_url']
            num_links = serializer.validated_data['num_links']

            task_id = str(uuid.uuid4())
            task = ScreenshotTask.objects.create(task_id=task_id)

            capture_screenshots.delay(task_id, start_url, num_links)

            return Response({"task_id": task_id}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ScreenshotListView(APIView):
    def get(self, request, task_id):
        task = get_object_or_404(ScreenshotTask, task_id=task_id)
        screenshots = task.screenshots.all()
        serializer = ScreenshotSerializer(screenshots, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
