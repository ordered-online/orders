from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/panel/(?P<panel_id>\w+)/$', consumers.PanelConsumer),
]
