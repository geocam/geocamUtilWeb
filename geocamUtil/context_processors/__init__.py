
from django.conf import settings as djangoSettings

def static(request):
    """
    Backport django.core.context_processors.static to Django 1.2.
    """
    return {'STATIC_URL': djangoSettings.STATIC_URL}

def settings(request):
    return {'settings': djangoSettings}
