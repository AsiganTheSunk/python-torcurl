#!/usr/bin/env python

import threading
import os
import pycurl
from cStringIO import StringIO
from stem.control import Controller, Signal
from bs4 import BeautifulSoup
from urllib import urlencode
from fake_useragent import UserAgent
from main.listeners import ExitRelayListener as erl
import subprocess
from time import sleep


class Response(str):
    def __new__(cls, code, type, data):
        return str.__new__(cls, data)

    def __init__(self, code, type, data):
        self.code = code
        self.type = type
        self.data = data
        str.__init__(self)

class ProxyChain():
    def __init__(self):
        return

# TODO PROBAR A QUE RECIBAN EL HANDLER; PARA VER SI SOLVENTA EL PROBLEMA DE TENER QUE REINSTANCIARLO.

class TorPyCurl():
    def __init__(self, ctrl_port=9051):
        self.handler = pycurl.Curl()

        # TODO, read from file.conf
        self.ctrl = Controller.from_port(port=ctrl_port)
        self.ctrl.authenticate(password='ultramegachachi')

        # Setup TempFile:
        self.tmpfile = str(os.getcwd() + '/file.tmp')

    def reset_handler(self):
        self.handler.close()
        self.handler = pycurl.Curl()


    def _proxy_setup(self, proxy='127.0.0.1', proxy_port=9050):
        # Setup tor curl options
        self.handler.setopt(pycurl.PROXY, proxy)
        self.handler.setopt(pycurl.PROXYPORT, proxy_port)
        self.handler.setopt(pycurl.PROXYTYPE, pycurl.PROXYTYPE_SOCKS5_HOSTNAME)

    def _curl_setup(self,url, headers={}, attrs={}, ssl=True, timeout=15, user_agent=str(UserAgent().random)):
        if attrs:
            url = "%s?%s" % (url, urlencode(attrs))

        self.handler.setopt(pycurl.URL, str(url))

        headers = map(lambda val: "%s: %s" % (val, headers[val]), headers)
        self.handler.setopt(pycurl.HTTPHEADER, headers)

        self.handler.setopt(pycurl.TIMEOUT, timeout)
        self.handler.setopt(pycurl.SSL_VERIFYPEER, ssl)
        self.handler.setopt(pycurl.USERAGENT, user_agent)

    def _curl_perform(self):
        response_buffer = StringIO()

        self.handler.setopt(pycurl.WRITEFUNCTION, response_buffer.write)
        self.handler.perform()

        code = self.handler.getinfo(pycurl.RESPONSE_CODE)
        type = self.handler.getinfo(pycurl.CONTENT_TYPE)
        data = response_buffer.getvalue()

        response_buffer.close()
        return Response(code, type, data)


    def get(self, url='https://check.torproject.org/', headers={}, attrs={}, ssl=True, timeout=15):

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

    def delete(self, url, attrs={}, headers={}, ssl=True, timeout=15):

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

    def reset(self):
        try:
            print('TorPyCurl Status: Connection Reset ExitRelay')
            self.ctrl.signal(Signal.NEWNYM)

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






