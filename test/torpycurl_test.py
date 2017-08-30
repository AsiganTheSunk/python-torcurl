#!/usr/bin/env python

from main.TorPyCurl import TorPyCurl
from main.ProxyRotator import ProxyRotator

def test0_create_torpycurl():
    tpc = TorPyCurl()
    assert tpc != None


def test0_get_request():
    proxy_rotator = ProxyRotator()
    session = TorPyCurl(proxy_rotator=proxy_rotator)
    response = session.get(url='https://httpbin.org/get')
    assert response.code == 200


def test0_post_request():
    proxy_rotator = ProxyRotator()
    session = TorPyCurl(proxy_rotator=proxy_rotator)
    url = 'https://httpbin.org/post'
    headers = {'Content-type': 'application/json', 'Accept': 'application/json'}
    data = {"From": "user@example.com", "To": "receiver@example.com", "Subject": "Pycurl", "TextBody": "Some text"}

    response = session.post(url=url, headers=headers, attrs=data)
    assert response.code == 200

def test0_put_request():
    proxy_rotator = ProxyRotator()
    session = TorPyCurl(proxy_rotator=proxy_rotator)
    url = 'https://httpbin.org/put'
    headers = {'Content-type': 'application/json', 'Accept': 'application/json'}

    response = session.put(url=url, headers=headers)
    assert response.code == 200

def test0_delete_request():
    proxy_rotator = ProxyRotator()
    session = TorPyCurl(proxy_rotator=proxy_rotator)
    url = 'https://httpbin.org/delete'
    headers = {'Content-type': 'application/json', 'Accept': 'application/json'}
    response = session.delete(url=url, headers=headers)
    assert response.code == 200
    return

def test0_login_request():
    return
