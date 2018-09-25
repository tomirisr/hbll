"""Core app urls"""
from django.conf.urls import url

from .views import HealthCheckView, IndexView

urlpatterns = [
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^status/health/$', HealthCheckView.as_view(), name='status-health'),
]
