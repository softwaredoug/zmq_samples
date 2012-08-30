import zmq
import sys

ctx = zmq.Context()
sock = ctx.socket(zmq.REQ)
port = int(sys.argv[1])
sock.connect("tcp://localhost:%i" % port)

echoTxt = sys.argv[-1]

while True:
    sock.send(echoTxt)
    echoedBack = sock.recv()
    print ">%s" % echoedBack