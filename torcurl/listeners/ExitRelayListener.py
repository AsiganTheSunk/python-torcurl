#!/usr/bin/env python

import functools
import os
from stem import StreamStatus
from stem.control import EventType, Controller
from time import sleep

from ExitRelay import ExitRelay

class ExitRelayListener():
    def __init__(self):
        print("TorPyCurl Status: Tracking Tor Exit...")

        self.controller = Controller.from_port()
        self.controller.authenticate('ultramegachachi')
        stream_listener = functools.partial(self.stream_event, self.controller)
        self.controller.add_event_listener(stream_listener, EventType.STREAM)
        sleep(10)

    def stream_event(self, controller, event):
        if event.status == StreamStatus.SUCCEEDED and event.circ_id:
            circ = controller.get_circuit(event.circ_id)

            exit_fingerprint = circ.path[-1][0]
            exit_relay = controller.get_network_status(exit_fingerprint)

            #print("Exit relay for our connection to %s" % (event.target))
            #print("  address: %s:%i" % (exit_relay.address, exit_relay.or_port))
            #print("  fingerprint: %s" % exit_relay.fingerprint)
            #print("  nickname: %s" % exit_relay.nickname)
            #print("  locale: %s" % controller.get_info("ip-to-country/%s" % exit_relay.address, 'unknown'))

            result = ExitRelay(exit_relay=str(event.target),
                               exit_address=(str(exit_relay.address) + ':' + str(exit_relay.or_port)),
                               exit_fingerprint=str(exit_relay.fingerprint), exit_nickname=str(exit_relay.nickname),
                               exit_locale=str(controller.get_info('ip-to-country/%s' % exit_relay.address, 'unknown')))

            result.save()
            #print(result)
            return
        return