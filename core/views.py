"""Main views for the core app for room_reservation project."""
import logging

from django.conf import settings
from django.db import connections
from django.db.utils import OperationalError
from django.http import JsonResponse
from django.shortcuts import render
from django.utils import timezone
from django.views import View

import requests

logger = logging.getLogger(__name__)


class IndexView(View):
    """Landing page for the room_reservation project."""

    def get(self, request):
        """Simple render of index.html template on a GET request."""
        return render(request, 'index.html')


class HealthCheckView(View):
    """
    Status health check view.

    Adds methods that follow the naming convention `check_[name]` to add new
    checks.

    See the `check_cas` and `check_default_db` method below for examples.
    """

    def get(self, request):
        """
        DON'T EDIT THIS METHOD.

        Add methods below called check_[name]. They should only take self and
        should return something that can be json serializable. See
        check_default_db or check_cas methods below for examples.
        """
        health = {'datetime': timezone.now()}
        methods = (m for m in dir(self) if m.startswith('check_'))

        for check_method in methods:
            key = check_method.replace('check_', '')
            health[key] = getattr(self, check_method)()

        return JsonResponse(health)

    def check_cas(self):
        cas_url = settings.CAS_SERVER_URL
        resp = requests.get(cas_url)
        return {
            'url': cas_url,
            'status_code': resp.status_code,
            'status': 'up' if resp.status_code == 200 else 'down',
        }

    def check_default_db(self):
        return self._check_database('default')

    def _check_database(self, alias):
        """
        This is not a check_ method, it is a helper method to make checking
        any database connection simple. See check_default_db for an example
        use.
        """
        conn = connections[alias]
        result = {
            'engine': settings.DATABASES[alias]['ENGINE'],
            'host': settings.DATABASES[alias]['HOST'],
            'name': settings.DATABASES[alias]['NAME'],
            'status': 'unknown',
        }

        try:
            conn.cursor()
        except OperationalError:
            result['status'] = 'down'
        else:
            result['status'] = 'up'

        return result
