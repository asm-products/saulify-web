import hashlib
import base64
import random
import time
from flask import g, Response, request
from saulify import app
from functools import wraps

def api_key_gen():
    hash_key = hashlib.sha256(str(random.getrandbits(256))).digest()
    rand_symb = random.choice(['rA', 'aZ', 'gQ', 'hH', 'hG', 'aR', 'DD'])
    return base64.b64encode(hash_key, rand_symb).rstrip('==')

# May it be "clean" function here (from view show_article)

'''
The rating code is based on http://python-eve.org/

BSD License

Copyright (c) 2014 by Nicola Iarocci and contributors. See AUTHORS for more details.

Some rights reserved.
'''
#
# class RateLimit(object):
#     """ Implements the Rate-Limiting logic using Redis as a backend.
#
#     :param key: the key used to uniquely identify a client.
#     :param limit: requests limit, per period.
#     :param period: limit validity period
#     :param send_x_headers: True if response headers are supposed to include
#                            special 'X-RateLimit' headers
#
#     .. versionadded:: 0.0.7
#     """
#     # Maybe has something complicated problems.
#
#     def __init__(self, key, limit, period, send_x_headers=True):
#         self.reset = int(time.time()) + period
#         self.key = key
#         self.limit = limit
#         self.period = period
#         self.send_x_headers = send_x_headers
#         p = app.redis.pipeline()
#         p.incr(self.key)
#         p.expireat(self.key, self.reset)
#         self.current = p.execute()[0]
#
#     remaining = property(lambda x: x.limit - x.current)
#     over_limit = property(lambda x: x.current > x.limit)
#
#
# def get_rate_limit():
#     """ If available, returns a RateLimit instance which is valid for the
#     current request-response.
#
#     .. versionadded:: 0.0.7
#     """
#     return getattr(g, '_rate_limit', None)
#
#
# def ratelimit():
#     """ Enables support for Rate-Limits on API methods
#     The key is constructed by default from the remote address or the
#     authorization.username if authentication is being used. On
#     a authentication-only API, this will impose a ratelimit even on
#     non-authenticated users, reducing exposure to DDoS attacks.
#
#     Before the function is executed it increments the rate limit with the help
#     of the RateLimit class and stores an instance on g as g._rate_limit. Also
#     if the client is indeed over limit, we return a 429, see
#     http://tools.ietf.org/html/draft-nottingham-http-new-status-04#section-4
#
#     .. versionadded:: 0.0.7
#     """
#     def decorator(f):
#         @wraps(f)
#         def rate_limited(*args, **kwargs):
#             req_method = request.headers.get('X-HTTP-Method-Override', request.method)
#             method_limit = app.config.get('RATE_LIMIT_' + req_method)
#             if method_limit and app.redis:
#                 limit = method_limit[0]
#                 period = method_limit[1]
#                 # If authorization is being used the key is 'username'.
#                 # Else, fallback to client IP.
#                 key = 'rate-limit/%s' % (
#                                          request.remote_addr)
#                 rlimit = RateLimit(key, limit, period, True)
#                 if rlimit.over_limit:
#                     return Response('Rate limit exceeded', 429)
#                 # store the rate limit for further processing by
#                 # send_response
#                 g._rate_limit = rlimit
#             else:
#                 g._rate_limit = None
#             return f(*args, **kwargs)
#         return rate_limited
#     return decorator
#
# def add_limit_rates_headers(resp):
#     '''
#     Add the response headers indicating the amount of limits the client still has to call.
#     This should be called last when sending the response to the user
#
#     :param resp: response object
#     :return: resp with added headers
#     '''
#     limit = get_rate_limit()
#     # if there is a limit and it is configured to set the headers
#     if limit and limit.send_x_headers:
#         resp.headers.add('X-RateLimit-Remaining', str(limit.remaining))
#         resp.headers.add('X-RateLimit-Limit', str(limit.limit))
#         resp.headers.add('X-RateLimit-Reset', str(limit.reset))
#     return resp

class RateLimit(object):
    expiration_window = 10

    def __init__(self, key_prefix, limit, per, send_x_headers):
        self.reset = (int(time.time()) // per) * per + per
        original = int(time.time())
        print 'tempo %s' %original
        print 'differenca %s' %(self.reset - original)
        print 'calculo tempo %s' % ((int(time.time()) // per) * per + per)
        self.key = key_prefix + str(self.reset)
        print 'key %s' %self.key
        self.limit = limit
        self.per = per
        self.send_x_headers = send_x_headers
        p = app.redis.pipeline()
        p.incr(self.key)
        p.expireat(self.key, self.reset + self.expiration_window)
        current =p.execute()[0]
        print 'current %s' %current
        self.current = current

    remaining = property(lambda x: x.limit - x.current)
    over_limit = property(lambda x: x.current >= x.limit)

def get_view_rate_limit():
    return getattr(g, '_view_rate_limit', None)

def on_over_limit(limit):
    return 'You hit the rate limit', 429

def ratelimit(limit, per=300, send_x_headers=True,
              over_limit=on_over_limit,
              scope_func=lambda: request.remote_addr,
              key_func=lambda: request.endpoint):
    def decorator(f):
        @wraps(f)
        def rate_limited(*args, **kwargs):
            key = 'rate-limit/%s/%s/' % (key_func(), scope_func())
            print 'funcao chamada'
            print 'key %s' %key
            rlimit = RateLimit(key, limit, per, send_x_headers)
            g._view_rate_limit = rlimit
            if over_limit is not None and rlimit.over_limit:
                return over_limit(rlimit)
            return f(*args, **kwargs)
        return rate_limited
    return decorator