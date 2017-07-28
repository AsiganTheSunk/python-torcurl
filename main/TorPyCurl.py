#!/usr/bin/env python

import threading
import os
import pycurl
import cStringIO
from stem.control import Controller, Signal
from bs4 import BeautifulSoup
from urllib import urlencode
import listeners.exit_relay_listener
import subprocess
from fake_useragent import UserAgent


class TorPyCurl():
    def __init__(self, proxy_port=9050, ctrl_port=9051, password=None):
        self.proxy_port = proxy_port
        self.ctrl_port = ctrl_port

        # Setup Stem Options:
        self.ctrl = Controller.from_port(port=self.ctrl_port)
        self.ctrl.authenticate(password='ultramegachachi')

        # Setup TempFile:
        self.tmpfile = str(os.getcwd() + '/file.tmp')

    def post(self, data={'field': 'value'}, url=None, ssl=True, timeout=15):
        curl = pycurl.Curl()

        # Setup common Curl options
        curl.setopt(pycurl.URL, url)
        curl.setopt(pycurl.TIMEOUT, timeout)
        curl.setopt(pycurl.SSL_VERIFYPEER, ssl)

        # Setup Tor related Curl options
        curl.setopt(pycurl.PROXY, '127.0.0.1')
        curl.setopt(pycurl.PROXYPORT, self.proxy_port)
        curl.setopt(pycurl.PROXYTYPE, pycurl.PROXYTYPE_SOCKS5_HOSTNAME)

        try:
            # Form data must be provided already urlencoded.
            postfields = urlencode(data)
            # Sets request method to POST,
            # Content-Type header to application/x-www-form-urlencoded
            # and data to send in request body.
            curl.setopt(curl.POSTFIELDS, postfields)
            curl.perform()

        except pycurl.error, error:
            errno, errstr = error
            print 'An error occurred: ', errstr

        finally:
            curl.close()




    def get(self, url='https://check.torproject.org/', ssl=True, timeout=15):
        # Creating Curl instance
        curl = pycurl.Curl()

        # Setup StringIO buffer
        buf = cStringIO.StringIO()
        curl.setopt(pycurl.WRITEFUNCTION, buf.write)

        # Setup common Curl options
        curl.setopt(pycurl.URL, url)
        curl.setopt(pycurl.TIMEOUT, timeout)
        curl.setopt(pycurl.SSL_VERIFYPEER, ssl)

        # Setup Tor related Curl options
        curl.setopt(pycurl.PROXY, '127.0.0.1')
        curl.setopt(pycurl.PROXYPORT, self.proxy_port)
        curl.setopt(pycurl.PROXYTYPE, pycurl.PROXYTYPE_SOCKS5_HOSTNAME)

        if not url:
            buf.close()
            curl.close()
            self.validate()

        else:
            try:
                curl.perform()
                html_doc = buf.getvalue()
                #print html_doc
                return html_doc

            except pycurl.error, error:
                errno, errstr = error
                print 'An error occurred: ', errstr

            finally:
                buf.close()
                curl.close()


    def validate(self, url='https://check.torproject.org/', ssl=True, timeout=15):
        # Creating Curl instance
        curl = pycurl.Curl()

        # Setup StringIO buffer
        buf = cStringIO.StringIO()
        curl.setopt(pycurl.WRITEFUNCTION, buf.write)

        # Setup common Curl options
        curl.setopt(pycurl.URL, url)
        curl.setopt(pycurl.TIMEOUT, timeout)
        curl.setopt(pycurl.SSL_VERIFYPEER, ssl)

        # Setup Tor related Curl options
        curl.setopt(pycurl.PROXY, '127.0.0.1')
        curl.setopt(pycurl.PROXYPORT, self.proxy_port)
        curl.setopt(pycurl.PROXYTYPE, pycurl.PROXYTYPE_SOCKS5_HOSTNAME)

        try:
            curl.perform()
            html_doc = buf.getvalue()
            soup = BeautifulSoup(html_doc, 'html.parser')
            #print soup
            status = soup.findAll('h1', {'class': 'not'})
            current_address = soup.findAll('p')[0]
            print 'TorPyCurl Connection address: ' + str(current_address.strong.text)

            if 'Congratulations.' in str(status[0].text).strip():
                print 'TorPyCurl Connection status: OK'
            else:
                print 'TorPyCurl Connection status: FAIL'

        except pycurl.error, error:
            errno, errstr = error
            print 'An error occurred: ', errstr

        finally:
            buf.close()
            curl.close()

    def reset(self):
        try:
            self.ctrl.authenticate(password="ultramegachachi")
            print('TorPyCurl Connection status: RESET EXIT RELAY')
            self.ctrl.signal(Signal.NEWNYM)

        except pycurl.error, error:
            errno, errstr = error
            print 'An error occurred: ', errstr

    def exits(self, url='https://check.torproject.org/exit-addresses'):
        return BeautifulSoup(self.get(url=url), 'html.parser')


    # Retrieve information about the Exit Node TODO
    def status(self):
        try:
            #t = threading.Thread(target=listeners.stream_listener.main())
            #t.start()

            listeners.exit_relay_listener.main()
            #subprocess.call('curl --socks5 127.0.0.1:9050 https://check.torproject.org', shell=True)
        except pycurl.error, error:
            errno, errstr = error
            print 'An error occurred: ', errstr


    # TODO
    # Permitir multiples hilos de Tor, en un futuro
    # Mirar que funcionalidades se le pueden implementar
    # No hacer overkill, de momento lo que tienes te llega!!
    # Grab stdout line by line as it becomes available.  This will loop until
    # p terminates.