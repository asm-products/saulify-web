from flask import url_for
from BeautifulSoup import BeautifulSoup
from flask.ext.login import current_user
from saulify.scrapers import cascade


def test_status_code(client):
    assert client.get(url_for('login')).status_code == 200


def test_login(client, add_user):
    lg = client.post('/login', data=dict(email='test@saulify.me',
                     password='test'), follow_redirects=True)
    assert lg.status_code == 200
    assert current_user.email == 'test@saulify.me'
    soup = BeautifulSoup(lg.data)
    labels = soup.findAll('p')
    for p in labels:
        print p.text
        if 'email' in p.text.lower():
            assert p.text.split(':')[1] == add_user['email']
        elif 'api' in p.text.lower():
            assert p.text.split(':')[1] == ''


def test_incorrect_login(client):
    lg = client.post('/login', data=dict(email='test@saulify.me',
                     password='incorrect'), follow_redirects=True)
    assert lg.status_code == 200
    assert current_user.is_active() is False


def test_user_page(client):
    up = client.get(url_for('user'))
    print 'unauthorized code {}'.format(up.status_code)
    assert up.status_code == 401


def test_logout(client):
    client.post('/login', data=dict(email='test@saulify.me',
                password='test'), follow_redirects=True)
    client.get(url_for('logout'), follow_redirects=True)
    assert current_user.is_active() is False


def test_create_api_key(client):
    client.post('/login', data=dict(email='test@saulify.me',
                password='test'), follow_redirects=True)
    print 'before create:{}'.format(current_user.api_key)
    assert current_user.api_key is None
    client.put('/user/key')
    print 'after create:{}'.format(current_user.api_key)
    assert current_user.api_key


def test_revoke_api_key(client):
    client.post('/login', data=dict(email='test@saulify.me',
                password='test'), follow_redirects=True)
    print 'before delete:{}'.format(current_user.api_key)
    assert current_user.api_key
    client.delete('/user/key')
    print 'after delete:{}'.format(current_user.api_key)
    assert current_user.api_key is None

def test_show_article_markdown(webtest_app):
    """This test just does some quick checks to make sure the page shows us the info we want.
    They could be made more accurate in the future, but there's a fine line between accurate tests and brittle tests.
    """
    page_to_markdownify = 'http://example.com'
    resp = webtest_app.get(url_for('show_article_markdown', u=page_to_markdownify))
    cleaned = cascade.clean_url(page_to_markdownify)
    assert cleaned["markdown"] in resp.body
    assert cleaned['title'] in resp.body


def test_clean_no_redirect(webtest_app):
    url = 'http://example.com'
    cleaned = cascade.clean_url(url)
    for false_arg in ['no', '0', 'false']:
        resp = webtest_app.get(url_for('show_article', u=url, short=false_arg))
        assert cleaned["markdown_html"] in resp.body

def test_clean_and_shorten_url(webtest_app):
    url = "http://example.com"
    cleaned = cascade.clean_url(url)
    resp = webtest_app.get(url_for('show_article', u=url))

    assert resp.status_int == 302
    assert len(resp.location) < url

    resp2 = webtest_app.get(resp.location)
    assert cleaned['markdown_html'] in resp2.body