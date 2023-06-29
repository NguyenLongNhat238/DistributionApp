import json
from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer, WebsocketConsumer
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from asgiref.sync import async_to_sync, sync_to_async


class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]
        if self.user.is_authenticated:
            await self.channel_layer.group_add(
                f"notification_user{self.user.id}", self.channel_name
            )
            await self.accept()
            await self.send_status()
        else:
            await self.close()

    async def receive(self, text_data=None, bytes_data=None, **kwargs):
        print(text_data)
        return await self.send(text_data=json.dumps({"text": "we got you"}))

    async def disconnect(self, code):
        await self.channel_layer.group_discard("notification", self.channel_name)
        await self.send_status()

    async def send_status(self):
        users = User.objects.all()
        html_users = render_to_string("includes/users.html", {"users": users})
        await self.channel_layer.group_send(
            "notification",
            {"type": "user_update", "event": "Change Status", "html_users": html_users},
        )

    # send message notification to user subscribe this channel if someone send message to them
    async def send_message_notification(self, event):
        await self.send_json(event)
        print("user_update", event)
