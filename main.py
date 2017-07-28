#!/usr/bin/env python

from main import TorPyCurl as tpc

def main():

    session = tpc.TorPyCurl()
    session.validate()
    session.reset()
    session.validate()
    # session.post()
    # session.exits()
    # session.status()


if __name__ == '__main__':
     main()
