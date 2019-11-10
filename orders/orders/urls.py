"""orders URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from . import views


urlpatterns = [
    path('admin/', admin.site.urls),

    path('orders/sessions/create/', views.create_session, name="create_session"),
    path('orders/sessions/get/<session_code>/', views.get_session, name="get_session"),
    path('orders/sessions/close/<session_code>/', views.close_session, name="close_session"),
    path('orders/create/', views.create_order, name="create_order"),
    path('orders/sessions/monitor/<session_code>/', views.monitor_session, name="monitor_session")
]
