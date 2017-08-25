#!/usr/bin/env python


import os, pycurl
from cStringIO import StringIO
from urllib import urlencode
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from main.exceptions import *
from main.Response import Response
from main.ProxyRotator import ProxyRotator
from main.listeners import ExitRelayListener as erl


LOCAL_HOST = '127.0.0.1'

class TorPyCurl():
    """Class

    Attributes:
    """
    def __init__(self, proxy_rotator = ProxyRotator):
        self.proxy_rotator = proxy_rotator
        self.handler = pycurl.Curl()

        # TODO read configuration from *.conf
        # TODO cypher the password... plx not in clarinete

    def reset_handler(self):
        """Function

        Attributes:
        """
        self.handler.close()
        self.handler = pycurl.Curl()


    def _proxy_setup(self, proxy=LOCAL_HOST, proxy_port=9050):
        """Function

        Attributes:
            proxy       -- proxy ip, by default loopback interface
            proxy_port  -- number of proxy port
        """

        tor_instance = self.proxy_rotator.get_tor_instance()
        tor_instance.add_connection_use_count()

        # Setup tor curl options
        tor_proxy_port = tor_instance.proxy_port
        tor_proxy_ip = tor_instance.proxy_ip

        self.handler.setopt(pycurl.PROXY, tor_proxy_ip)
        self.handler.setopt(pycurl.PROXYPORT, tor_proxy_port)
        self.handler.setopt(pycurl.PROXYTYPE, pycurl.PROXYTYPE_SOCKS5_HOSTNAME)

    def _curl_setup(self,url, headers={}, attrs={}, ssl=True, timeout=15, user_agent=str(UserAgent().random)):
        """Function

        Attributes:
            url     --
            headers --
            attrs   --
            ssl     --
            timeout --
            user_agent  --
        """

        if attrs:
            url = "%s?%s" % (url, urlencode(attrs))

        self.handler.setopt(pycurl.URL, str(url))

        headers = map(lambda val: "%s: %s" % (val, headers[val]), headers)
        self.handler.setopt(pycurl.HTTPHEADER, headers)

        self.handler.setopt(pycurl.TIMEOUT, timeout)
        self.handler.setopt(pycurl.SSL_VERIFYPEER, ssl)
        self.handler.setopt(pycurl.USERAGENT, user_agent)

    def _curl_perform(self):
        """Function

        Attributes:
        """

        response_buffer = StringIO()

        self.handler.setopt(pycurl.WRITEFUNCTION, response_buffer.write)
        self.handler.perform()

        code = self.handler.getinfo(pycurl.RESPONSE_CODE)
        type = self.handler.getinfo(pycurl.CONTENT_TYPE)
        data = response_buffer.getvalue()

        response_buffer.close()

        return Response(code, type, data)


    def get(self, url='https://check.torproject.org/', headers={}, attrs={}, ssl=True, timeout=15):
        """Function

        Attributes:
            url     --
            headers --
            attrs   --
            ssl     --
            timeout --
        """

        # Reset of the Curl instance, to ensure that the new exitRelay works properly
        self.reset_handler()

        # Set request type: GET
        self.handler.setopt(pycurl.HTTPGET, True)

        # Common
        self._proxy_setup()
        self._curl_setup(url=url, headers=headers, attrs=attrs, ssl=ssl, timeout=timeout)

        try:
            return self._curl_perform()

        except pycurl.error, error:
            errno, errstr = error
            print 'An error occurred: ', errstr

    def post(self, url=None, headers={}, attrs={},  ssl=True, timeout=15):
        """Function

        Attributes:
            url     --
            headers --
            attrs   --
            ssl     --
            timeout --
        """

        # Reset of the Curl instance, to ensure that the new exitRelay works properly
        self.reset_handler()

        # Set request type: POST
        self.handler.setopt(pycurl.POST, True)
        self.handler.setopt(pycurl.POSTFIELDS, urlencode(attrs))

        # Common
        self._proxy_setup()
        self._curl_setup(url=url, headers=headers, attrs=attrs, ssl=ssl, timeout=timeout)


        try:
            return self._curl_perform()

        except pycurl.error, error:
            errno, errstr = error
            print 'An error occurred: ', errstr

    def put(self, url, headers={}, attrs={}, ssl=True, timeout=15):
        """Function

        Attributes:
            url     --
            headers --
            attrs   --
            ssl     --
            timeout --
        """

        # Reset of the Curl instance, to ensure that the new exitRelay works properly
        self.reset_handler()

        # Set request type: PUT
        encoded_attrs = urlencode(attrs)
        request_buffer = StringIO(encoded_attrs)

        self.handler.setopt(pycurl.PUT, True)
        self.handler.setopt(pycurl.READFUNCTION, request_buffer.read)
        self.handler.setopt(pycurl.INFILESIZE, len(encoded_attrs))

        # Common
        self._proxy_setup()
        self._curl_setup(url=url, headers=headers, attrs=attrs, ssl=ssl, timeout=timeout)

        try:
            return self._curl_perform()

        except pycurl.error, error:
            errno, errstr = error
            print 'An error ocurred: ', errstr

    def delete(self, url, headers={}, attrs={}, ssl=True, timeout=15):
        """Function

        Attributes:
            url     --
            headers --
            attrs   --
            ssl     --
            timeout --
        """

        # Reset of the Curl instance, to ensure that the new exitRelay works properly
        self.reset_handler()

        # Set request type: DELETE
        self.handle.setopt(pycurl.CUSTOMREQUEST, 'DELETE')

        # Common
        self._proxy_setup()
        self._curl_setup(url=url, headers=headers, attrs=attrs, ssl=ssl, timeout=timeout)

        try:
            return self._curl_perform()

        except pycurl.error, error:
            errno, errstr = error
            print 'An error ocurred: ', errstr


    def validate(self, url='https://check.torproject.org/', ssl=True, timeout=15):
        """Function

        Attributes:
            url     --
            ssl     --
            timeout --
        """

        try:
            response = self.get(url=url, ssl=ssl, timeout=timeout)
            soup = BeautifulSoup(response.data, 'html.parser')

            status = soup.findAll('h1', {'class': 'not'})
            current_address = soup.findAll('p')[0]

            print 'TorPyCurl Connection address: ' + str(current_address.strong.text)

            if 'Congratulations.' in str(status[0].text).strip():
                print 'TorPyCurl Status: Connection PASS'
            else:
                print 'TorPyCurl Status: Connection FAIL'

        except pycurl.error, error:
            errno, errstr = error
            print 'An error occurred: ', errstr



    def dns_leak_test(self, url='https://www.perfect-privacy.com/check-ip/', ssl=True, timeout=15):
        #POST y 2 coockies hacen falta al menos. usar tamper data

        """Function

        Attributes:
            url     --
            ssl     --
            timeout --
        """

        try:
            response = self.get(url=url, ssl=ssl, timeout=timeout)
            soup = BeautifulSoup(response.data, 'html.parser')
            '''
            token = (soup.findAll('a', {'id': 'startbtn'}))[0]['href']

            print str(url+token)
            response = self.post(url=url+token,ssl=ssl, timeout=timeout)
            sleep(5)
            response = self.get(url=url + token, ssl=ssl, timeout=timeout)
            '''
            soup = BeautifulSoup(response.data, 'html.parser')
            print soup
            info = soup.findAll('table')
            print info

            #print 'TorPyCurl Connection address: ' + str(current_address.strong.text)

            #if 'Congratulations.' in str(status[0].text).strip():
            #    print 'TorPyCurl Status: Connection PASS'
            #else:
            #    print 'TorPyCurl Status: Connection FAIL'

        except pycurl.error, error:
            errno, errstr = error
            print 'An error occurred: ', errstr


    def exits(self, url='https://check.torproject.org/exit-addresses'):
        return BeautifulSoup(self.get(url=url), 'html.parser')

    # TODO Grab stdout line by line as it becomes available.
    # TODO Retrieve information about the Exit Node in a more reliable way
    def status(self):
        try:
            erl.ExitRelayListener()
        except pycurl.error, error:
            errno, errstr = error
            print 'An error occurred: ', errstr





