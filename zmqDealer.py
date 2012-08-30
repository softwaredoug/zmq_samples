import zmq
import sys
import itertools

ctx = zmq.Context()
sock = ctx.socket(zmq.DEALER)

for port in sys.argv[1:-1]:
    sock.connect("tcp://localhost:%i" % int(port))
echoText = sys.argv[-1]

for i in itertools.count():
    print "Sending..."
    # When a ZMQ_DEALER socket is connected to a ZMQ_REP socket each message 
    # sent must consist of an empty message part, the delimiter, followed by one or more body parts.
    sock.send("", zmq.SNDMORE) 
    print "Sending more..."
    sock.send(echoText + "(%i)" % i)
    print "Receiving..."
    echoTextBack = sock.recv()
    print "> %s" % echoTextBack
