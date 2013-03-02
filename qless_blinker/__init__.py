#!/usr/bin/env python

import sys
import qless

class QlessBlinkerClient( qless.client):
    def __init__( self, *args, **kwargs):
        super( QlessBlinkerClient, self).__init__( *args, **kwargs)

        arr = sys.argv[0].split("/")[-1].split(".")
        if len(arr) > 1:
            self.script_name = arr[-2]
        else:
            self.script_name = arr[-1]

        self.worker_name = "%s:%s" % (self.worker_name, self.script_name)
