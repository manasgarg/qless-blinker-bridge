A bridge between qless & blinker
================================

The idea is simple: raise a signal from one application through the blinker
library and receive it in another application through the blinker library.

qless does the job of transferring the signal from one application to another
application.

Dependencies
============

It works with gevent library. If you don't want that, feel free fork and remove
the dependency.

How to use it
=============

Let's say, you have 2 applications: SignalSender & SignalReceiver1 & SignalReceiver2.

Let's also say that you want to route the signal "user-object-updated" to both the receivers.

Step1
=====
Decide the qless queue names for both the receivers. Let's say, SignalReceiver1
will use the queue name "signal-receiver-1" and SignalReceiver2 will use the
queue name "signal-receiver-2".

Step 2
======

In SignalSender, you execute this code at the startup:

from qless_blinker.sender import route_signal
route_signal( "user-object-updated", ["signal-receiver-1", "signal-receiver-2"])

When you execute this code, this library will start listening for the signal
"user-object-updated" and whenever that signal is raised, it will put the
signal & the associated data on the "signal-receiver-1" & "signal-receiver-2"
queues.

Step 3
======

In SignalReceiver1, you execute this code at startup:

from qless_blinker.receiver import listen_on_queue
listen_on_queue( "signal-receiver-1")

In SignalReceiver2, you execute this code at startup:

from qless_blinker.receiver import listen_on_queue
listen_on_queue( "signal-receiver-2")

Done
====

That's it. Now whenever you raise the signal "user-object-updated" in
SignalSender application, it will also be received in the receiver
applications.
