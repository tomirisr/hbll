import logging

from django.conf import settings
from django.contrib import admin

logger = logging.getLogger(__name__)

title = settings.CONFIG.safe(
    'meta/project_name', default=settings.PROJECT_NAME
).title()
admin.site.site_title = f'{title} administration'
admin.site.site_header = admin.site.site_title
