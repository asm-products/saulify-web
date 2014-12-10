import hashlib
import base64
import random
import time
from flask import g, request
from saulify import app
from functools import wraps
from flask.ext.login import current_user


def api_key_gen():
    hash_key = hashlib.sha256(str(random.getrandbits(256))).digest()
    rand_symb = random.choice(['rA', 'aZ', 'gQ', 'hH', 'hG', 'aR', 'DD'])
    return base64.b64encode(hash_key, rand_symb).rstrip('==')

# May it be "clean" function here (from view show_article)

'''
The rating code is based on
http://flask.pocoo.org/snippets/70/ and http://python-eve.org/
'''


class RateLimit(object):
    """ Implements the Rate-Limiting logic using Redis as a backend.

    :param key_prefix: the key used to uniquely identify a client.
    :param limit: requests limit, per period.
    :param per: limit validity period
    :param send_x_headers: True if response headers are supposed to include
                           special 'X-RateLimit' headers
    """
    expiration_window = 10

    def __init__(self, key_prefix, limit, per, send_x_headers):
        self.reset = (int(time.time()) // per) * per + per
        self.key = key_prefix + str(self.reset)
        self.limit = limit
        self.per = per
        self.send_x_headers = send_x_headers
        p = app.redis.pipeline()
        p.incr(self.key)
        p.expireat(self.key, self.reset + self.expiration_window)
        self.current = p.execute()[0]

    remaining = property(lambda x: max(0, x.limit - x.current))
    over_limit = property(lambda x: x.current > x.limit)


def get_rate_limit():
    """ If available, returns a RateLimit instance which is valid for the
    current request-response.
    """
    return getattr(g, '_rate_limit', None)


def on_over_limit(rlimit):
    """
    The answer when the limit is set. It would be better if it was a json.
    """
    return 'You hit the rate limit', 429

# types of limit
LIMIT_METHOD_API = 0
LIMIT_METHOD_USER = 1
LIMIT_METHOD_IP = 2


def ratelimit(limit, per=300, send_x_headers=True, method=LIMIT_METHOD_API,
              over_limit=on_over_limit,
              key_func=lambda: request.endpoint):
    """ Enables support for Rate-Limits on API methods
    The key is constructed by default from the remote address or the
    authorization.username if authentication is being used. On
    a authentication-only API, this will impose a ratelimit even on
    non-authenticated users, reducing exposure to DDoS attacks.

    Before the function is executed it increments the rate limit with the help
    of the RateLimit class and stores an instance on g as g._rate_limit. Also
    if the client is indeed over limit, we return a 429, see
    http://tools.ietf.org/html/draft-nottingham-http-new-status-04#section-4

    should ALWAYS be put after the decorator require_appkey

    use: @ratelimit(limit=2, per=60) - number of calls per seconds

    :param limit: the number of calls to be accepted
    :param per (optional): the windows in seconds
    :param send_x_headers(optional): should put the limit headers on response
    :param method (optional): API_KEY,
    :param over_limit(optional): a function with the asnwer when the limit is reached
    :param key_func(optional): function with the endpoint being called
    """
    def decorator(f):
        @wraps(f)
        def rate_limited(*args, **kwargs):
            # check what kind of key should be used
            user = current_user
            key = None
            if method == LIMIT_METHOD_API:
                # get the key from the URL
                key = request.args.get('key')
            elif (method == LIMIT_METHOD_USER) and user.is_authenticated():
                key = user.username()

            # did not worked, get by ip
            if not key:
                key = request.remote_addr

            # define the key and save in global to use later
            key = 'rate-limit/%s/%s/' % (key_func(), key)
            rlimit = RateLimit(key, limit, per, send_x_headers)
            g._rate_limit = rlimit
            if over_limit is not None and rlimit.over_limit:
                return over_limit(rlimit)
            return f(*args, **kwargs)
        return rate_limited
    return decorator
