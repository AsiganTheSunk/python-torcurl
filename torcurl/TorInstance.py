#!/usr/bin/env python

from stem.control import Controller, Signal
import time
from colorama import Fore, Style

DEFAULT_PROXY_PORT = 9050
DEFAULT_CNTRL_PORT = 9051
DEFAULT_TIME_OUT_RESET_THRESHOLD = 180
DEFAULT_RESET_THRESHOLD = 30
DEFAULT_CIRCUIT_HOPS = 'X'
LOCAL_HOST = '127.0.0.1'

UPPER_TIMER_LIMIT = 600
LOWER_TIMER_LIMIT = 300

# force circuit extension to provide n jumps if needed when the tor instance it's created.
# force exit policy to the socket to provide some security
# force country exit node policy to provide additional control over where you are hopping.
# Threaded in the future...

class TorInstance():
    """Class

        Attributes:
        """

    def __init__(self, tor_instance_id, nickname, proxy_port, cntrl_port, exit_policy, circuit_hops):
        self.tor_instance_id = tor_instance_id
        self.proxy_ip = LOCAL_HOST
        self.cntrl_port = cntrl_port
        self.proxy_port = proxy_port
        self.nickname = nickname
        self.exit_policy =  exit_policy # controller.set_conf("ExitNodes", "{" + country + "}")
        self.circuit_hops = circuit_hops
        self.country_list = 'ALL'
        self.circuit_dirtyness = time.time()
        self.ctrl = Controller.from_port(port=cntrl_port)
        self.ctrl.authenticate(password='dummypass')

        if circuit_hops is None:
            self.circuit_hops = DEFAULT_CIRCUIT_HOPS


        # Aditional Configuration. Even tho the circuits resets every 10min, we are gonna force a higher refresh if it's
        # needed or upon reaching the max number of connections per circuit that it's stablished by the attr connection_reset_threshold

        self.time_out_reset_threshold = DEFAULT_TIME_OUT_RESET_THRESHOLD
        self.connection_reset_threshold = DEFAULT_RESET_THRESHOLD
        self.connection_count = 0
        return


    def __str__(self):
        timer = time.time()
        return('TorInstance ID: %s\n Nickname: %s\n ProxyPort: %s, CntrlPort: %s\n Circuit Dirt: %s, Circuit Hops: %s\n ExitPolicy: {%s}\n'
               ' Country List: %s' % (
                   self.tor_instance_id, self.nickname, self.proxy_port, self.cntrl_port, self.colored_dirtyness(timer - self.circuit_dirtyness), self.circuit_hops, self.exit_policy,
                   self.country_list
        ))

    def add_connection_use_count(self):
        """Function

            Attributes:
            """
        self.connection_count = self.connection_count + 1
        return

    def build_circuit(self):
        """Function

            Attributes:
            """
        #add the needed hops
        return

    def reset(self):
        """Function

        Attributes:
        """
        try:
            print('TorPyCurl Status: Connection Reset ExitRelay')
            self.ctrl.signal(Signal.NEWNYM)
        except:
            print 'An error occurred: '

    def colored_dirtyness(self, timer):

        if timer < LOWER_TIMER_LIMIT:
            return (Fore.LIGHTGREEN_EX + Style.DIM + 'CLEAN' + Style.RESET_ALL)
        elif timer < UPPER_TIMER_LIMIT:
            return (Fore.LIGHTMAGENTA_EX + Style.DIM + 'SEMI-CLEAN' + Style.RESET_ALL)
        else:
            return (Fore.LIGHTRED_EX + Style.DIM + 'DIRTY' + Style.RESET_ALL)
