#!/usr/bin/env python
from main.TorInstance import TorInstance

def test0_create_tor_instance():
    tor_instance = TorInstance(0, None, 9050, 9051, None, None)
    assert tor_instance != None

def test0_add_connetion_use_count():
    tor_instance = TorInstance(0, None, 9050, 9051, None, None)
    tor_instance.add_connection_use_count()
    assert tor_instance.connection_count != 0

def test0_build_circuit():
    tor_instance = TorInstance(0, None, 9050, 9051, None, None)
    return

def test0_rest_circuit():
    tor_instance = TorInstance(0, None, 9050, 9051, None, None)
    return

# fst test ip, snd test dns leak
def test0_validate_circuit():
    tor_instance = TorInstance(0, None, 9050, 9051, None, None)
    return

def test1_validate_circuit():
    tor_instance = TorInstance(0, None, 9050, 9051, None, None)
    return