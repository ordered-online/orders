from enum import Enum

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.forms import model_to_dict
from django.utils import timezone


class SessionState(Enum):
    OPEN = "OPEN"
    CLOSED = "CLOSED"

    @classmethod
    def choices(cls):
        return tuple((k.name, k.value) for k in cls)


class Session(models.Model):
    # mandatory fields
    code = models.CharField(max_length=6, primary_key=True)
    name = models.TextField(max_length=200)
    location_id = models.IntegerField()

    # optional fields
    state = models.CharField(max_length=255, choices=SessionState.choices(), default=SessionState.OPEN.value)

    # autogenerated fields
    timestamp = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ["name", "location_id"]
        indexes = [
            models.Index(fields=["location_id"]),
            models.Index(fields=["state"]),
        ]

    @property
    def accepts_orders(self):
        return not self.state == SessionState.CLOSED

    @property
    def dict_representation(self):
        session_dict = model_to_dict(self)
        session_dict["orders"] = [
            order.dict_representation for order in self.order_set.all()
        ]
        session_dict["timestamp"] = session_dict["timestamp"].isoformat()
        return session_dict

    @property
    def group_name(self):
        return "session_{}".format(self.code)

    def broadcast_session_update(self):
        """Broadcast session updates to the channel layer."""
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            self.group_name, {"type": "session_update", "session": self.dict_representation}
        )


@receiver(post_save, sender=Session, dispatch_uid="session_post_save")
def session_post_save(sender, instance, **kwargs):
    instance.broadcast_session_update()


class Order(models.Model):

    # mandatory fields
    product_id = models.IntegerField()
    session = models.ForeignKey(Session, on_delete=models.CASCADE)

    # autogenerated fields
    timestamp = models.DateTimeField(default=timezone.now)

    class Meta:
        indexes = [
            models.Index(fields=["session"])
        ]

    @property
    def dict_representation(self):
        order_dict = model_to_dict(self)
        order_dict["timestamp"] = order_dict["timestamp"].isoformat()
        return order_dict


@receiver(post_save, sender=Order, dispatch_uid="order_post_save")
def order_post_save(sender, instance, **kwargs):
    instance.session.broadcast_session_update()
