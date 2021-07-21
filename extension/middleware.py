from django.http import HttpResponseForbidden
from admin_honeypot.models import LoginAttempt
from .response import ErrorResponse
from config import settings


class BlockedIpMiddleware(object):
    """
    middleware for block bot and attacker that attack to site
    by admin-honeypot and they are that in bot_block_ip(config.settings)
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # block black list in admin-honeypot
        for i in LoginAttempt.objects.all():
            if request.META['REMOTE_ADDR'] not in i.ip_address:
                return ErrorResponse(message='You are a Hacker!', status=403).send()
        response = self.get_response(request)
        return response


class BlockedIpBotUserAgentMiddleware(object):
    """
    check user agent and if have not user agent ==> return Forbiden
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        scrapy_user_agent = 'Scrapy/VERSION (+https://scrapy.org)'
        # is_test_server in config/settings/__init__.py for test productions
        if not settings.is_test_server:
            if 'HTTP_USER_AGENT' not in request.META:
                return ErrorResponse(message='You are a Robot!', status=403).send()
            else:
                user_agent = request.META['HTTP_USER_AGENT']
                if user_agent == scrapy_user_agent:
                    return ErrorResponse(message='You are a Robot!', status=403).send()

        response = self.get_response(request)
        return response
