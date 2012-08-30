import zmq
import sys

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