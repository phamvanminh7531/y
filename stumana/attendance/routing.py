from django.urls import path
from .consumers import AttendanceConsumer


ws_urlpatterns = [
    path('ws/attendance/', AttendanceConsumer.as_asgi())
]