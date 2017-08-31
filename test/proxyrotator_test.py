#!/usr/bin/env python

from torcurl.ProxyRotator import ProxyRotator

def test0_create_proxy_rotator():
    proxy_rotator = ProxyRotator()
    assert proxy_rotator != None

def test0_get_tor_instance():
    proxy_rotator = ProxyRotator()
    tor_instance = proxy_rotator.get_tor_instance()
    tor_instance_id = tor_instance.tor_instance_id
    assert tor_instance_id == 0

def test0_eval_tor_instance():
    proxy_rotator = ProxyRotator()
    tor_instance = proxy_rotator.get_tor_instance()
    result = proxy_rotator.eval_tor_instance(tor_instance)
    assert True == result

def test1_eval_tor_instance():
    proxy_rotator = ProxyRotator()
    tor_instance = proxy_rotator.get_tor_instance()
    tor_instance.connection_count = 60
    result = proxy_rotator.eval_tor_instance(tor_instance)
    assert False == result