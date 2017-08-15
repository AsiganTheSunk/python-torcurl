#!/usr/bin/env python

from main import TorPyCurl as tpc
from main.listeners import ExitRelayListener as erl
import threading
from time import sleep

def main():


    session = tpc.TorPyCurl()
    session.validate()
    session.reset()
    session.validate()

    #session2 = tpc.TorPyCurl()
    #session2.validate()
    #session.status()






if __name__ == '__main__':
     main()

