#!/usr/bin/env python

from main import TorPyCurl as tpc
from main.exceptions.exceptions import UrlValueError, Error
from main.listeners import ExitRelayListener as erl
import threading
from time import sleep

from main.ProxyRotator import TorInstance
from main.ProxyRotator import ProxyRotator


def main():
    session = tpc.TorPyCurl()
    session.validate()
    session.dns_leak_test()
    # session.reset()
    # session.validate()

    try:
        '''
        proxyRotator = ProxyRotator()
        proxyRotator._add_tor_instance(None, 9060, 9061, None, None)
        proxyRotator._add_tor_instance(None, 9070, 9071, None, None)
        proxyRotator._add_tor_instance(None, 9080, 9080, None, None)
        proxyRotator.eval_tor_instance()

        for index in range(0, 3):
            torinstance = proxyRotator.get_tor_instance()
            proxyRotator.increment_connection_count(tor_instance_id=torinstance.tor_instance_id)

        proxyRotator.eval_tor_instance()

        for index in range(0, 3):
            torinstance = proxyRotator.get_tor_instance()
            proxyRotator.increment_connection_count(tor_instance_id=torinstance.tor_instance_id)

        proxyRotator.eval_tor_instance()
        #raise Error('This is an error')
<<<<<<< Updated upstream
        #raise UrlValueException()
        
        print proxyRotator
        '''
=======
        raise UrlValueError()
>>>>>>> Stashed changes
    except Error, arg:
        print 'Error: ', arg.msg


if __name__ == '__main__':
     main()

