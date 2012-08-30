import zmq
import sys
import itertools
from zmqUtils import sendAll, recvAll
from cmdPromptUtils import waitExit
# These are simple samples, so for the sake of clarity, there's 
# not a whole lot of error checking. They eschew the more advanced
# features of 0mq in preference to demonstrating core concepts.
#
# This code demonstrates ZMQ_DEALER. For more information on
# the behavior of a DEALER socket, check the zmq_socket
# man page: http://api.zeromq.org/2-1:zmq-socket under the
# heading for ZMQ_DEALER

if len(sys.argv) < 3:
    print "usage zmqDealerTimeoutWork.py <port0> ... <portN> echoTxt"
    waitExit()

ctx = zmq.Context()
sock = ctx.socket(zmq.DEALER)

for port in sys.argv[1:-1]:
    print "Connecting to port %i" % int(port)
    sock.connect("tcp://localhost:%i" % int(port))
echoText = sys.argv[-1]

class TimeoutError(Exception):
    pass

def timeoutRcv(sock,timeoutMsec):
    """ Timeout on work by using the timeout
        in poll"""
    poller = zmq.Poller()
    poller.register(sock, zmq.POLLIN)
    socks = dict(poller.poll(timeout=timeoutMsec))
    if sock in socks:
        if socks[sock] == zmq.POLLIN:
            return sock.recv()
    else:
        raise TimeoutError

for i in itertools.count():
    print "Sending..."
    currEchoText = echoText + ("(%i)" % i)
    sock.send(currEchoText)
    # When connecting to a ZMQ_REP, an empty delimiter must be sent,
    # See the zmq_socket man page for more info
    #sendAll(sock, ["", currEchoTxt]) 
    print "Receiving..."
    try:
        echoTextBack = timeoutRcv(sock, timeoutMsec=1000)
        print "> %s" % echoTextBack
    except TimeoutError:
        print "! %s TimedOut!" % currEchoText
        
waitExit()