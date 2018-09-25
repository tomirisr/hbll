from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin

from core import urls as core_urls

urlpatterns = [
    # Django Admin
    url(r'^admin/', include(admin.site.urls)),
    # Django Hijack
    url(r'^hijack/', include('hijack.urls')),
    # Core app urls
    url(r'^', include(core_urls)),
]

if settings.CAS_ENABLED:
    from cas.views import login as login_view
    from cas.views import logout as logout_view

    urlpatterns += [
        # CAS Authentication Endpoints
        url(settings.LOGIN_URL_REGEX, login_view, name='login'),
        url(settings.LOGOUT_URL_REGEX, logout_view, name='logout'),
    ]

if settings.DEBUG:
    from django.views import defaults as view_defaults
    import debug_toolbar

    kwargs = {'exception': Exception()}
    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
        # This allows the error pages to be debugged during development, just
        # visit these url in browser to see what these error pages look like.
        url(r'^400/$', view_defaults.bad_request, kwargs),
        url(r'^403/$', view_defaults.permission_denied, kwargs),
        url(r'^404/$', view_defaults.page_not_found, kwargs),
        url(r'^500/$', view_defaults.server_error),
    ]
