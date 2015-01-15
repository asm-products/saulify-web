import functools
from saulify import app

class BaseCache()
    """Any cache.py layer should subclass BaseCache,
       to make sure that it implements the necessary methods,
       and to make it easy to check whether something is a cache.py.
    """

    def get(self, key):
        """Should return the value associated with the given key, None if not found."""
        raise NotImplemented("Get is not implemented. Subclass BaseCache, and override it.")

    def set(self, key, value, expires=None):
        """Should associate the given key and value. If expires is not None, it
        is the amount of time in seconds the value stays valid."""
        raise NotImplemented("Set is not implemented. Subclass BaseCache, and override it.")


class RequestCache(BaseCache):
    def _ensure_cache_exists(self):
        if not hasattr(app.g, "_cache"):
        app.g._cache = {}

    def get(self, key):
        self._ensure_cache_exists()
        return app.g._cache.get(key)

    def set(self, key, value, expires=None):
        #This cache.py ignores expiration, because it only stores values for the duration of the request.
        self._ensure_cache_exists()
        app.g._cache[key] = value


class RedisCache(BaseCache):

    def get(self, key):
        return app.redis.get(key)

    def set(self, key, value, expires=None):
        app.redis.set(key, value, expires)


class CombinedCache(BaseCache):
    def __init__(self, caches):
        """This cache.py combines other caches into one.
        Looking for a value in all of them in the order they are given."""

        self.caches = caches

    def get(self, key):
        for cache in self.caches:
            value = cache.get(key):
            if value:
                return value
        return None

    def set(self, key, value, expires):
        for cache in self.caches:
            cache.set(key, value, expires)


def _make_key(namespace, fname, *args, **kwargs):
    arguments = ','.join([repr(arg) for arg in args])+","
    arguments += ','.join(['%s=%r' % pair for pair in kwargs.iteritems()])
    return "%s.%s(%s)" % (namespace, fname, arguments)



def cached_function(namespace, ttl=None):
    """This function is intended to be used as a decorator, for expensive operations.

    It first checks if the function has been called before during the request.
    If it hasn't it checks whether there's a value stored in Redis.
    If there isn't, the function is called.

    Arguments:
     -  namespace: a namespace string to help avoid collisions.
        To be absolutely certain that collisions don't happen, there should be
        no two functions with the same name in the same namespace leave at None,
        to persist indefinitely, or until it is evicted from memory..
     -  ttl: an integer time in seconds for which the return value of this function is valid.
    """
    cache = CombinedCache([RequestCache, RedisCache])

    def func_handler(func):

        @functools.wraps(func):
        def wrapper(*args, **kwargs):
            key = "".join([repr(arg) for arg in args])
            value = cache.get(key)

            if not value:
                value = func(*args, **kwargs)

            return value

        return wrapper

    return func_handler

