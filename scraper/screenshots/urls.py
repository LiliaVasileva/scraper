from django.urls import path
from .apis import IsAliveView, ScreenshotCreateView, ScreenshotListView

urlpatterns = [
    path('isalive/', IsAliveView.as_view(), name='isalive'),
    path('screenshots/', ScreenshotCreateView.as_view(), name='screenshot-create'),
    path('screenshots/<str:task_id>/', ScreenshotListView.as_view(), name='screenshot-list'),
]