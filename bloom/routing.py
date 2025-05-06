from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'^ws/garden/(?P<garden_id>\d+)/$', consumers.GardenConsumer.as_asgi()),
]