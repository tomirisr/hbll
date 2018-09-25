import logging

from django.apps import AppConfig

logger = logging.getLogger(__name__)


class CoreConfig(AppConfig):
    name = 'core'
    verbose_name = 'room_reservation'

    def ready(self):
        from . import signals  # noqa
