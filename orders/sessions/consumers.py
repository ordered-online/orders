import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer


class SessionConsumer(WebsocketConsumer):
    def connect(self):
        self.session_id = self.scope["url_route"]["kwargs"]["session_id"]
        self.session_group_name = "session_%s" % self.session_id

        # join session group
        async_to_sync(self.channel_layer.group_add)(
            self.session_group_name, self.channel_name
        )

        self.accept()

        self.send({
            "info": "Connection was successful. Assigned to session group: {}"
            .format(self.session_group_name)
        })

    def disconnect(self, code):
        async_to_sync(self.channel_layer.group_discard)(
            self.session_group_name, self.channel_name
        )

    def session_message(self, event):
        message = event["message"]

        # forward message to websocket
        self.send(text_data=json.dumps({
            "message": message
        }))
