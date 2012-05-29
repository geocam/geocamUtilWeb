
from django.conf import settings

def static(request):
    """
    Backport django.core.context_processors.static to Django 1.2.
    """
    return {'STATIC_URL': settings.STATIC_URL}

    def request(request):
        return {'request': request}
