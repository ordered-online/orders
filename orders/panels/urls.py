from django.urls import path

from orders import settings

from . import views


urlpatterns = []

if settings.DEBUG:
    urlpatterns.append(
        path('debug/<panel_id>/', views.debug_panel)
    )
