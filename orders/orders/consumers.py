import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

from .models import Session


class SessionConsumer(WebsocketConsumer):

    def connect(self):
        self.session_code = self.scope["url_route"]["kwargs"]["session_code"]
        self.session_group_name = "session_%s" % self.session_code

        # reject all connections to erroneous session codes
        try:
            self.session = Session.objects.get(code__exact=self.session_code)
        except Session.DoesNotExist as e:
            self.close()
            return

        # join session group
        async_to_sync(self.channel_layer.group_add)(
            self.session_group_name, self.channel_name
        )

        self.accept()

        self.send(text_data=json.dumps(self.session.dict_representation))

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