#!/usr/bin/env python

from blinker import signal
import qless
import uuid
import time

import logging
logger = logging.getLogger(__name__)

from qless_blinker import QlessBlinkerClient
import qless_blinker.receiver

signal_queue_map = {}

qless_client = QlessBlinkerClient()

signal_list = []
class SignalListener(object):
    def __init__( self, signal_name):
        self.signal_name = signal_name

    def __call__( self, sender, **kwargs):
        event_data = {"event_id": uuid.uuid4().hex, "timestamp": time.time(), "sender": str(sender), "signal_name": self.signal_name}
        event_data.update( kwargs)

        logger.debug("Routing blinker signal %s: %s" % (self.signal_name, str( event_data)))

        for queue_name in signal_queue_map[self.signal_name]:
            queue = qless_client.queues[queue_name]
            queue.put( qless_blinker.receiver.EventReceiver, event_data, jid=event_data["event_id"], retries=10)

def listen_for_signal( signal_name):
    s = signal( signal_name)
    s.connect( SignalListener(signal_name), weak=False)
    signal_list.append( s)

def route_signal( signal_name, queue_list):
    if not signal_queue_map.has_key( signal_name):
        signal_queue_map[signal_name] = set()
        listen_for_signal( signal_name)
        logger.debug("Listening for signal %s to route it on queues: %s" % (signal_name, ', '.join(queue_list)))

    signal_queue_map[signal_name].update( queue_list)
