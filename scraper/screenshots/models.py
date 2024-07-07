from django.core.files.storage import FileSystemStorage
from django.db import models
from config.django.settings import MEDIA_ROOT

fs = FileSystemStorage(location=str(MEDIA_ROOT / 'screenshots'))


class ScreenshotTask(models.Model):
    task_id = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)


class Screenshot(models.Model):
    task = models.ForeignKey(ScreenshotTask, related_name='screenshots', on_delete=models.CASCADE)
    url = models.URLField()
    image = models.ImageField(storage=fs)
    created_at = models.DateTimeField(auto_now_add=True)
