from django.http import HttpResponseForbidden
from admin_honeypot.models import LoginAttempt


class BlockedIpMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        for i in LoginAttempt.objects.all():
            if request.META['REMOTE_ADDR'] not in i.ip_address:
                return HttpResponseForbidden('<h1>Forbidden</h1>')
        response = self.get_response(request)
        return response
