#!/usr/bin/env python

from main import TorPyCurl as tpc
from main.exceptions.exceptions import UrlValueException, Error
from main.listeners import ExitRelayListener as erl
import threading
from time import sleep


def main():
    # session = tpc.TorPyCurl()
    # session.validate()
    # session.reset()
    # session.validate()

    try:
        #raise Error('This is an error')
        raise UrlValueException()
    except Error, arg:
        print 'Error: ', arg.msg


if __name__ == '__main__':
     main()

