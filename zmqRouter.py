import zmq
import signal
import sys
import cmdPromptUtils
from zmqUtils import sendAll, recvAll

if len(sys.argv) < 2:
    print "usage zmqRouter.py <bindPort>"
    cmdPromptUtils.waitExit()

context = zmq.Context()
port = int(sys.argv[1])

frontend = context.socket(zmq.ROUTER)
print "Binding to port %i" % port
frontend.bind("tcp://*:%i" % port)

allParts = ()

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