import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer


class PanelConsumer(WebsocketConsumer):
    def connect(self):
        self.panel_id = self.scope["url_route"]["kwargs"]["room_name"]
        self.panel_group_name = "panel_%s" % self.panel_id

        # join panel group
        async_to_sync(self.channel_layer.group_add)(
            self.panel_group_name, self.channel_name
        )

        self.accept()

        self.send({
            "info": "Connection was successful. Assigned to panel group: {}"
            .format(self.panel_group_name)
        })

    def disconnect(self, code):
        async_to_sync(self.channel_layer.group_discard)(
            self.panel_group_name, self.channel_name
        )

    def panel_message(self, event):
        message = event["message"]

        # forward message to websocket
        self.send(text_data=json.dumps({
            "message": message
        }))
