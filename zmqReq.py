import zmq
import sys
import cmdPromptUtils
# These are simple samples, so for the sake of clarity, there's 
# not a whole lot of error checking. They eschew the more advanced
# features of 0mq in preference to demonstrating core concepts.
#
# This code demonstrates ZMQ_REQ (request) socket. For more information on
# the behavior of a REQ socket, check the zmq_socket
# man page: http://api.zeromq.org/2-1:zmq-socket under the
# heading for ZMQ_REQ
#
# Since CtrlC generally doesn't work, I recommend forking
# these from your shell (ie start zmqReq.py <port> on Windows
# or zmqReq.py <port>

if len(sys.argv) < 3:
    print "usage zmqReq.py <connectPort0> .. <connectPortN> <echoTxt>"
    cmdPromptUtils.waitExit()

# Boilerplate zmq code, create a context and 
# a socket of that specific type from that context
ctx = zmq.Context()
sock = ctx.socket(zmq.REQ)
port = int(sys.argv[1])

# Connect to the ports specified
# on the command prompt
for port in sys.argv[1:-1]:
    sock.connect("tcp://localhost:%i" % int(port))

# Grab the text the user wants us to echo
echoTxt = sys.argv[-1]

# A REQ socket can only send/recv serially
# trying to do send after a send, or a second
# recv results in a ZMQError exception
while True:
    print "Sending %s" % echoTxt
    sock.send(echoTxt) # send the request
    print "Receiving..."
    echoedBack = sock.recv()
    print ">%s" % echoedBack