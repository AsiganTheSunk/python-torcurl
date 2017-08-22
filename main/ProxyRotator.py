#!/usr/bin/env python

import random
from main.TorInstance import TorInstance

DEFAULT_PROXY_PORT = 9050
DEFAULT_CNTRL_PORT = 9051
DEFAULT_ID = 1
DEFAULT_INSTANCE_NICK_NAMES = ['Moctezuma','Catherine','Ghandi', 'Ragnar', 'Tokugawa', 'Sitting Bull', 'Joao II']


class ProxyRotator():
    """Class

    Attributes:
    """
    def __init__(self):
        self.tor_instance_list = []
        self.tor_connection_mode = 'Random'
        self.tor_instance_list.append(TorInstance(DEFAULT_ID, DEFAULT_INSTANCE_NICK_NAMES[0] ,DEFAULT_PROXY_PORT, DEFAULT_CNTRL_PORT, None, None))
        self.tor_instance_counter = len(self.tor_instance_list)
        return

    def __str__(self):
        result = '\nProxyRotator Instance\n Number of Instances: %s, Connection Mode: %s\n' %\
                 (self.tor_instance_counter, self.tor_connection_mode)
        for item in self.tor_instance_list:
            result = result + '\n' + str(item) + '\n'
        return(result)


    def _add_tor_instance(self, nickname, proxy_port, cntrl_port, exit_policy, circuit_hops):
        """Function

            Attributes:
            """

        if nickname is None:
            nickname = DEFAULT_INSTANCE_NICK_NAMES[self.tor_instance_counter]
        self.tor_instance_list.append(TorInstance(self._new_tor_instance_id(), nickname, proxy_port, cntrl_port, exit_policy, circuit_hops))
        return

    def _new_tor_instance_id(self):
        """Function

            Attributes:
            """

        instance_id = self.tor_instance_counter = self.tor_instance_counter + 1
        return instance_id


    def get_tor_instance(self):
        """Function

            Attributes:
            """

        return random.choice(self.tor_instance_list)


    def eval_tor_instance(self):
        """Function

            Attributes:
            """

        # Move here the evaluation of the tor exit
        # Move here the dns leak test, to try to evade problems before using the connection circuit.

        for tor_instance in self.tor_instance_list:
            if tor_instance.connection_count == 4:
                print '[ %s ]: %s - %s >> Circuit should reset shortly...' % (tor_instance.nickname, tor_instance.proxy_port, tor_instance.cntrl_port)
            else:
                print '[ %s ]: %s - %s >> Circuit connection count: %s' % (tor_instance.nickname, tor_instance.proxy_port, tor_instance.cntrl_port, tor_instance.connection_count)
        return


    def increment_connection_count(self, tor_instance_id):
        """Function

            Attributes:
            """

        for tor_instance in self.tor_instance_list:
            if tor_instance.tor_instance_id == tor_instance_id:
                tor_instance.increment_connection_count()
                print '[ %s ]: %s - %s >> ++Circuit connection count: %s' % (tor_instance.nickname, tor_instance.proxy_port, tor_instance.cntrl_port, tor_instance.connection_count)
                return
        return