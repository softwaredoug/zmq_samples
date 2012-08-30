import zmq
import sys
import cmdPromptUtils

if len(sys.argv) < 2:
    print "usage zmqRep.py <bindPort>"
    cmdPromptUtils.waitExit()

cmdPromptUtils.promptExitOnSigInt()


ctx = zmq.Context()
sock = ctx.socket(zmq.REP)

port = int(sys.argv[1])
print "binding to port %i" % port
sock.bind("tcp://*:%i" % port)

while True:
    print "Receiving..."
    echoData = sock.recv()
    print "Sending... %s" % echoData
    sock.send(echoData)