import json
from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer, WebsocketConsumer
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from asgiref.sync import async_to_sync, sync_to_async


class NewUserConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()
        async_to_sync(self.channel_layer.group_add)("users", self.channel_name)

        user = self.scope["user"]
        print(user)
        if user.is_authenticated:
            print("access")
            self.update_user_status(user, True)
            self.send_status()

    async def receive(self, text_data=None, bytes_data=None, **kwargs):
        print(text_data)
        return self.send(text_data=json.dumps({"text": "we got you"}))

    async def disconnect(self, code):
        async_to_sync(self.channel_layer.group_discard)("users", self.channel_name)

        user = self.scope["user"]
        if user.is_authenticated:
            self.update_user_status(user, False)
            self.send_status()

    async def send_status(self):
        users = User.objects.all()
        html_users = render_to_string("includes/users.html", {"users": users})
        self.channel_layer.group_send(
            "users",
            {"type": "user_update", "event": "Change Status", "html_users": html_users},
        )

    async def user_update(self, event):
        self.send_json(event)
        print("user_update", event)

    def update_user_status(self, user, status):
        print("Oke")
        user.status = status
        user.save()
        return user


class ChatConsumer(WebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.room_name = None
        self.room_group_name = None
        self.room = None
        self.user = None  # new
        self.user_inbox = None  # new

    def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"
        self.user = self.scope["user"]  # new
        self.user_inbox = f"inbox_{self.user.username}"  # new
        # connection has to be accepted
        self.accept()

        # join the room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name,
        )
        # send the user list to the newly joined user
        self.send(
            json.dumps(
                {
                    "type": "user_list",
                    "users": [user.username for user in self.room.online.all()],
                }
            )
        )

        if self.user.is_authenticated:
            # -------------------- new --------------------
            # create a user inbox for private messages
            async_to_sync(self.channel_layer.group_add)(
                self.user_inbox,
                self.channel_name,
            )
            # ---------------- end of new ----------------
            # send the join event to the room
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    "type": "user_join",
                    "user": self.user.username,
                },
            )

            self.room.online.add(self.user)

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name,
        )
        if self.user.is_authenticated:
            # -------------------- new --------------------
            # delete the user inbox for private messages
            async_to_sync(self.channel_layer.group_discard)(
                self.user_inbox,
                self.channel_name,
            )
            # ---------------- end of new ----------------
            # send the leave event to the room
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    "type": "user_leave",
                    "user": self.user.username,
                },
            )
            self.room.online.remove(self.user)

    def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        if not self.user.is_authenticated:  # new
            return  # new
        # -------------------- new --------------------
        if message.startswith("/pm "):
            split = message.split(" ", 2)
            target = split[1]
            target_msg = split[2]

            # send private message to the target
            async_to_sync(self.channel_layer.group_send)(
                f"inbox_{target}",
                {
                    "type": "private_message",
                    "user": self.user.username,
                    "message": target_msg,
                },
            )
            # send private message delivered to the user
            self.send(
                json.dumps(
                    {
                        "type": "private_message_delivered",
                        "target": target,
                        "message": target_msg,
                    }
                )
            )
            return
        # ---------------- end of new ----------------
        # send chat message event to the room
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                "type": "chat_message",
                "user": self.user.username,  # new
                "message": message,
            },
        )

    def chat_message(self, event):
        self.send(text_data=json.dumps(event))

    def user_join(self, event):
        self.send(text_data=json.dumps(event))

    def user_leave(self, event):
        self.send(text_data=json.dumps(event))

    def private_message(self, event):
        self.send(text_data=json.dumps(event))

    def private_message_delivered(self, event):
        self.send(text_data=json.dumps(event))
