#!/usr/bin/env python

import threading
import functools
from stem import StreamStatus
from stem.control import EventType, Controller
from listeners.ExitRelay import ExitRelay

class TorPyCurlListener():
    def __init__ (self, proxy_port=9050, ctrl_port=9051, password=None):
        self.proxy_port = proxy_port
        self.ctrl_port = ctrl_port

        # Setup Stem Options:
        self.ctrl = Controller.from_port(port=self.ctrl_port)
        self.ctrl.authenticate(password='ultramegachachi')

    def stream_event(self, event):
        if event.status == StreamStatus.SUCCEEDED and event.circ_id:
            circ = self.ctrl.get_circuit(event.circ_id)

            exit_fingerprint = circ.path[-1][0]
            exit_relay = self.ctrl.get_network_status(exit_fingerprint)

            print('Exit relay for our connection to %s' % (event.target) +
                  '\n address: %s:%i' % (exit_relay.address, exit_relay.or_port) +
                  '\n fingerprint: %s' % exit_relay.fingerprint +
                  '\n nickname: %s' % exit_relay.nickname +
                  '\n locale: %s' % self.ctrl.get_info('ip-to-country/%s' % exit_relay.address, 'unknown'))


            ExitRelay(exit_relay=str(event.target), exit_address=(str(exit_relay.address) + ':' + str(exit_relay.or_port)),
                      exit_fingerprint=str(exit_relay.fingerprint), exit_nickname=str(exit_relay.nickname),
                      exit_locale=str(self.ctrl.get_info('ip-to-country/%s' % exit_relay.address, 'unknown')))

            #


def main():
  print("Tracking requests for tor exits. Press 'enter' to end.")
  print("")


  listener = torpycurlListener().stream_event()
  with Controller.from_port() as controller:
    controller.authenticate('ultramegachachi')

    stream_listener = functools.partial(listener, controller)
    controller.add_event_listener(stream_listener, EventType.STREAM)


if __name__ == '__main__':
  main()