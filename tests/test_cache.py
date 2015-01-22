import mock
import pytest
from saulify import cache


def mock_out_redis(app, monkeypatch, return_value=None):
    """A helper that replaces redis with a mock."""
    redis_mock = mock.Mock()
    redis_mock.get = mock.Mock(return_value=return_value)
    redis_mock.set = mock.Mock()
    monkeypatch.setattr(app, "redis", redis_mock)
    return redis_mock

def test_cache_looks_in_request_cache_and_redis_before_calling_the_function(app, monkeypatch):

    redis_mock = mock_out_redis(app, monkeypatch)
    # TODO find a way to actually mock out flask.g. Mocking it out using mock.PropertyMock doesn't work.

    @cache.cached_function(namespace="test")
    def heavy_function(n):
        return 'foo'*n

    assert heavy_function(2) == "foofoo"
    assert redis_mock.get.call_count == 1
    assert redis_mock.set.call_count == 1


def test_cache_doesnt_look_in_redis_if_key_found_in_request_cache(app, monkeypatch):

    redis_mock = mock_out_redis(app, monkeypatch)

    @cache.cached_function(namespace="test")
    def expensive_function():
        return "foo"

    expensive_function()
    expensive_function()

    #It tries to get the value from redis the first time, the second time,
    # it should find the value in the request cache.
    assert redis_mock.get.call_count == 1


def test_cache_doesnt_call_function_if_value_is_in_redis(app, monkeypatch):
    mock_redis = mock_out_redis(app, monkeypatch, "expected_value")

    @cache.cached_function(namespace="test")
    def expensive_function():
        raise AssertionError("This function should not be called, the value it returns can be found in redis.")

    assert expensive_function() == "expected_value"
    assert mock_redis.get.call_count == 1

def test_integration(app, redis):
    # this test uses the redis server at TEST_REDIS_URL
    call_counter = mock.Mock(return_value="foo")
    func_mock = lambda : call_counter()

    expensive_function = cache.cached_function(namespace='test')(func_mock)

    assert expensive_function() == 'foo'
    assert expensive_function() == 'foo'

    assert call_counter.call_count == 1

def test_cache_uses_serializer(app, monkeypatch):
    mock_redis = mock_out_redis(app, monkeypatch, return_value=None)

    def serializer(s):
        return str(s)

    def deserializer(s):
        return int(s)

    @cache.cached_function(namespace="test", serializer=serializer, deserializer=deserializer)
    def expensive_function(x):
        return x*x

    assert expensive_function(3) == 9
    assert expensive_function(3) == 9 #ensure value is also deserialized on cache hit.
    assert mock_redis.set.call_args[0][1] == '9'

@pytest.mark.parametrize(
    'val,strval', [
        (3, '3'),
        (3.5, '3.5'),
        (True, 'True'),
        (None, 'None'),
        ('One does not simply test a cache.', "'One does not simply test a cache.'"),
        ([1, 'a', 3.5, None, False], "[1, 'a', 3.5, None, False]")
    ]
)
def test_serialize_and_unserialize_expression(val, strval):
    assert cache.serialize_expression(val) == strval
    assert cache.deserialize_expression(strval) == val