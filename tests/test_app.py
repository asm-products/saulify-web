from flask import url_for
from BeautifulSoup import BeautifulSoup
from flask.ext.login import current_user


def test_status_code(client):
    assert client.get(url_for('login')).status_code == 200


def test_login(client, add_user):
    lg = client.post('/login', data=dict(username='test',
                     password='test'), follow_redirects=True)
    assert lg.status_code == 200
    assert current_user.username == 'test'
    soup = BeautifulSoup(lg.data)
    labels = soup.findAll('p')
    for p in labels:
        print p.text
        if 'username' in p.text.lower():
            assert p.text.split(':')[1] == add_user['username']
        elif 'email' in p.text.lower():
            assert p.text.split(':')[1] == add_user['email']
        elif 'api' in p.text.lower():
            assert p.text.split(':')[1] == 'None'


def test_incorrect_login(client):
    lg = client.post('/login', data=dict(username='test',
                     password='incorrect'), follow_redirects=True)
    assert lg.status_code == 200
    assert current_user.is_active() is False


def test_user_page(client):
    up = client.get(url_for('user'))
    print 'unauthorized code {}'.format(up.status_code)
    assert up.status_code == 401


def test_logout(client):
    client.post('/login', data=dict(username='test',
                password='test'), follow_redirects=True)
    client.get(url_for('logout'), follow_redirects=True)
    assert current_user.is_active() is False


def test_create_api_key(client):
    client.post('/login', data=dict(username='test',
                password='test'), follow_redirects=True)
    print 'before create:{}'.format(current_user.api_key)
    assert current_user.api_key is None
    client.put('/user/key')
    print 'after create:{}'.format(current_user.api_key)
    assert current_user.api_key


def test_revoke_api_key(client):
    client.post('/login', data=dict(username='test',
                password='test'), follow_redirects=True)
    print 'before delete:{}'.format(current_user.api_key)
    assert current_user.api_key
    client.delete('/user/key')
    print 'after delete:{}'.format(current_user.api_key)
    assert current_user.api_key is None
