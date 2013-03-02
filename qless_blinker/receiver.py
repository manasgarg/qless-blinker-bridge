from blinker import signal
import qless
import uuid
import time
import gevent

import logging
logger = logging.getLogger(__name__)

from qless_blinker import QlessBlinkerClient

qless_client = QlessBlinkerClient()

class EventReceiver( object):
    @staticmethod
    def process( job):
        logger.debug("Converting qless event to blinker signal: %s" % str( job.data))

        try:
            s = signal(job["signal_name"])
            sender = job.data["sender"]
            del( job.data["sender"])
            s.send( sender, **job.data)
            job.complete()
        except:
            logger.exception( "Failed to execute job with data: %s" % job.data)
            job.fail( 'failed-jobs', "Job Failed")

def queue_listener( queue_name):
    queue = qless_client.queues[queue_name]
    while True:
        seen = False
        job = queue.pop()

        if job:
            seen = True
            job.process()

        if not seen:
            time.sleep( 2)

def do_process_old_jobs():
    jids = qless_client.workers[qless_client.worker_name]['jobs']
    while( len( jids)):
        job = qless_client.jobs[jids.pop(0)]
        job.process()

def process_old_jobs():
    gevent.spawn( do_process_old_jobs)

queue_list = []
def listen_on_queue( queue_name):
    import gevent

    if queue_name in queue_list:
        return

    queue_list.append( queue_name)
    gevent.spawn( queue_listener, queue_name)
