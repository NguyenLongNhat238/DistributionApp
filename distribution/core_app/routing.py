from core_app.consumers import NewUserConsumer
from django.urls import path, re_path


websocket_patterns = [
    re_path(r"new-user/$", NewUserConsumer.as_asgi()),
]
