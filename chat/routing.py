
from .consumers import Chat
from django.urls import path


websocket_urlpatterns = [
    path(r'chat/<int:room_id>/', Chat.as_asgi()),

]
