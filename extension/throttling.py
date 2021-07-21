from pytimeparse.timeparse import timeparse
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle


class CustomThrottlingUser(UserRateThrottle):
    """
    scope ==> for know that which class or url
    rate ==> THROTTLE_RATES in base.py
    use in /views.py
    """
    scope = 'apps'
    rate = '3/1s'

    def parse_rate(self, rate):
        """
        Given the request rate string, return a two tuple of:
        <allowed number of requests>, <period of time in seconds>
        """

        if rate is None:
            return None, None
        num, period = rate.split('/')
        num_requests = int(num)
        duration = timeparse(period)
        return num_requests, duration
