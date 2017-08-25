#!/usr/bin/env python

from main import TorPyCurl as tpc
from main.exceptions.exceptions import UrlValueError, Error
from main.listeners import ExitRelayListener as erl
from main.ProxyRotator import TorInstance
from main.ProxyRotator import ProxyRotator
from time import sleep

def main():
    try:
        proxyRotator = ProxyRotator()
        proxyRotator.add_tor_instance(None, 9060, 9061, None, None)
        proxyRotator.add_tor_instance(None, 9070, 9071, None, None)

        print 'SEQUENTIAL TEST'
        #proxyRotator.set_proxy_connection_mode(mode='sequential')
        session = tpc.TorPyCurl(proxy_rotator=proxyRotator)
        session.validate()
        sleep(2)
        session.validate()
        sleep(2)
        session.validate()
        sleep(2)
        session.validate()
        #print
        #print 'RANDOM TEST'
        #proxyRotator.set_proxy_connection_mode(mode='random')
        #session2 = tpc.TorPyCurl(proxy_rotator=proxyRotator)
        #session2.validate()
        #session2.validate()
        #session2.validate()

    except Error, arg:
        print 'Error: ', arg.msg


if __name__ == '__main__':
     main()

