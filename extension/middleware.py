from config.settings.base import BLOCKED_IPS
from django.http import HttpResponseForbidden


class BlockedIpMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.META['REMOTE_ADDR'] in BLOCKED_IPS:
            return HttpResponseForbidden('<h1>Forbidden</h1>')
        response = self.get_response(request)
        return response
