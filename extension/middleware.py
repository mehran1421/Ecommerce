from django.http import HttpResponseForbidden
from admin_honeypot.models import LoginAttempt
from config.settings.base import bot_block_ip


class BlockedIpMiddleware(object):
    """
    middleware for block bot and attacker that attack to site
    by admin-honeypot and they are that in bot_block_ip(config.settings)
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # block ip bot request
        if request.META['REMOTE_ADDR'] in bot_block_ip:
            return HttpResponseForbidden('<h1>Forbidden</h1>')

        # block black list in admin-honeypot
        for i in LoginAttempt.objects.all():
            if request.META['REMOTE_ADDR'] not in i.ip_address:
                return HttpResponseForbidden('<h1>Forbidden</h1>')
        response = self.get_response(request)
        return response


class BlockedIpBotUserAgentMiddleware(object):
    """
    check user agent and if it detects that it is a robot, add to bot_block_ip
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # android, windows, ios
        keywords = ['Mobile', 'Opera Mini', 'Android', 'iPhone', 'Mac', 'CPU', 'Windows', 'Phone', 'NT', 'Edge',
                    'Chrome', 'CrOS', 'Macintosh', ]

        user_agent = request.META['HTTP_USER_AGENT']

        # check if dont have user agent, add to bot_block_ip
        if [word in user_agent for word in keywords] is None:
            bot_block_ip.append(request.META['REMOTE_ADDR'])

        response = self.get_response(request)
        return response
