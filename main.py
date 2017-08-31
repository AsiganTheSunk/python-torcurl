#!/usr/bin/env python

from torcurl import TorPyCurl as tpc
from torcurl.exceptions.exceptions import UrlValueError, Error
from torcurl.listeners import ExitRelayListener as erl
from torcurl.ProxyRotator import TorInstance
from torcurl.ProxyRotator import ProxyRotator
from time import sleep
import json
from fake_useragent import UserAgent

def main():
    try:
        proxyRotator = ProxyRotator()
        session = tpc.TorPyCurl(proxy_rotator=proxyRotator)
        data = {"From": "user@example.com", "To": "receiver@example.com", "Subject": "Pycurl", "TextBody": "Some text"}
        headers = {'Content-type':'application/json','Accept':'application/json'}
        url = 'https://httpbin.org/post'

        response = session.post(url=url, headers=headers, attrs=data)
        print response.code
        print response.data

        url = 'https://httpbin.org/put'
        response = session.put(url=url, headers=headers)
        print response.code
        print response.data

        response = session.login()
        print response.code
        #print response.data

        '''
        
        
        proxyRotator.add_tor_instance(None, 9060, 9061, None, None)
        proxyRotator.add_tor_instance(None, 9070, 9071, None, None)

        print 'SEQUENTIAL TEST'
        proxyRotator.set_proxy_connection_mode(mode='sequential')
        session = tpc.TorPyCurl(proxy_rotator=proxyRotator)
        session.validate()
        session.validate()
        session.validate()
        session.validate()
        session.validate()
        session.validate()
        session.validate()
        session.validate()
        session.validate()


        print
        print 'RANDOM TEST'
        proxyRotator.set_proxy_connection_mode(mode='random')
        session2 = tpc.TorPyCurl(proxy_rotator=proxyRotator)
        #session2.validate()
        #session2.validate()
        #session2.validate()
        '''
    except Error, arg:
        print 'Error: ', arg.msg


if __name__ == '__main__':
     main()

