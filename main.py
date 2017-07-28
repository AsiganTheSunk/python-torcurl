#!/usr/bin/env python

from main import TorPyCurl as tpc
from main.listeners import ExitRelayListener as erl
import threading

def main():


    session = tpc.TorPyCurl()

    session.validate()
    session.reset()
    session.validate()
    session.status()





if __name__ == '__main__':
     main()

