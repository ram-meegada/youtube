from django.urls import path
from .consumers import ProgressUpdateConsumer 

websocket_urlpatterns = [
    path("progres-update/<str:uuid>/", ProgressUpdateConsumer.as_asgi())
]