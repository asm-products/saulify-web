from saulify import app as test_app
from saulify.common import ratelimit

@test_app.route('/test')
@ratelimit(2,60)
def test_route():
    '''
    a very simple route that will be called until it reach the limit
    '''
    return 'ok'

def test_shortener(client):
    # try once and than another 2 times to see if the return is ok.
    ret = client.get('/test', follow_redirects=True)
    assert ret.status_code == 200

    ret = client.get('/test', follow_redirects=True)
    assert ret.status_code == 200

    ret = client.get('/test', follow_redirects=True)
    assert ret.status_code == 429
