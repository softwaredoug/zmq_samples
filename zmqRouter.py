import zmq
import signal
import sys
import cmdPromptUtils
from zmqUtils import sendAll, recvAll
# These are simple samples, so for the sake of clarity, there's 
# not a whole lot of error checking. They eschew the more advanced
# features of 0mq in preference to demonstrating core concepts.
#
# This code demonstrates a ZMQ_ROUTER socket. For more information on
# the behavior of a ROUTER socket, check the zmq_socket
# man page: http://api.zeromq.org/2-1:zmq-socket under the
# heading for ZMQ_ROUTER
#
# Since CtrlC generally doesn't work, I recommend forking
# these from your shell (ie start zmqReq.py <port> on Windows
# or zmqReq.py <port> &)

if len(sys.argv) < 2:
    print "usage zmqRouter.py <bindPort>"
    cmdPromptUtils.waitExit()

# Boilerplate zmq code, create context and socket
context = zmq.Context()
port = int(sys.argv[1])

# Bind to the port specified in argv
frontend = context.socket(zmq.ROUTER)
print "Binding to port %i" % port
frontend.bind("tcp://*:%i" % port)

# A Router socket need is an asyncrhonous version of the REP
# socket. Instead of needing to serially process with recv/send/recv/send...
# A Router allows multiple simultaneous active requests. 
#
# To quote from the zmq_socket man page:
# > When receiving messages a ZMQ_ROUTER socket shall prepend a message 
# > part containing the identity of the originating peer to the message 
# > before passing it to the application. Messages received are fair-queued 
# > from among all connected peers. When sending messages a ZMQ_ROUTER socket
# > shall remove the first part of the message and use it to determine the 
# > identity of the peer the message shall be routed to. If the peer does
# > not exist anymore the message shall be silently discarded.
# 
# Below we wait for 2 requests before responding to the individual requests
while True:
    print "Get 2 requests"
    activeRequests = []
    for i in range(0,2):
        allParts = recvAll(frontend)
        activeRequests.append(allParts)
    print "Send 2 replies"
    for parts in activeRequests:
        print "Sending back %s" % repr(parts)
        sendAll(frontend, parts)