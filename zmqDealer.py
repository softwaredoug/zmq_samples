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
    print "usage zmqDealer.py <port0> ... <portN> echoTxt"
    waitExit()

# Boilerplate 0mq stuff, create a context and our socket
ctx = zmq.Context()
sock = ctx.socket(zmq.DEALER)

# Interpret everything from 1 ... just before the end as
# a candidate port
for port in sys.argv[1:-1]:
    sock.connect("tcp://localhost:%i" % int(port))
echoText = sys.argv[-1]

# A DEALER is an asynchronous REQ socket. Like a REQ socket it
# can connect to multiple hosts and will request from those
# hosts in a round-robin fashion. Unlike a REQ socket, the 
# responses are not processed serially but fair queued.
#
# To quote the man page:
# > Each message sent is round-robinned among all connected 
# > peers, and each message received is fair-queued from all 
# > connected peers.
#
# Another important note, sometimes the REQ and DEALER sockets
# get stuck if the other side crashes and the REQ or DEALER is
# stuck, so implementing a timeout (see zmqDealerTimeoutWork.py)
# for more.
for i in itertools.count():
    currEchoTxt = echoText + "(%i)" % i
    print "Sending... %s" % currEchoTxt
    # When connecting to a ZMQ_REP, an empty delimiter must be sent,
    # See the zmq_socket man page for more info
    sendAll(sock, ["", currEchoTxt]) 
    #sock.send(currEchoTxt)
    print "Receiving..."
    echoTextBack = recvAll(sock)
    print "Rcvd: > %s" % repr(echoTextBack)
    
waitExit()
