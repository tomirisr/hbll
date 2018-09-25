"""Permissions classes"""
import logging

from rest_framework import permissions

logger = logging.getLogger(__name__)


class HasAPIGroupPermission(permissions.BasePermission):
    """
    API permissions class that grants permission if the authenticated user is
    in a specific django auth group.

    The functionality of this permissions class can be customized by adding a
    `required_groups` attribute to the API view. This attribute should be a
    dict with a mapping from HTTP methods as the keys to a list of django auth
    group names that have permission for that method. For example:

        class MyAPIView(APIView):
            ...
            required_groups = {
                'GET': ['GetPeopleGroup', 'HeadPeopleGroup'],
                'POST': ['SecretPostGroup'],
            }
            ...

    By default the 'API' group is granted permission to all  HTTP methods.
    """

    def has_permission(self, request, view):
        """Override"""
        required_groups_mapping = getattr(view, 'required_groups', {})
        required_groups = required_groups_mapping.get(request.method, ['API'])
        return request.user.groups.filter(name__in=required_groups).count() > 0
