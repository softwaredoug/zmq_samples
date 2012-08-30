import zmq
import sys
import cmdPromptUtils
# These are simple samples, so for the sake of clarity, there's 
# not a whole lot of error checking. They eschew the more advanced
# features of 0mq in preference to demonstrating core concepts.
#
# This code demonstrates ZMQ_REP (reply) socket. For more information on
# the behavior of a REP socket, check the zmq_socket
# man page: http://api.zeromq.org/2-1:zmq-socket under the
# heading for ZMQ_REP
#
# Since CtrlC generally doesn't work, I recommend forking
# these from your shell (ie start zmqReq.py <port> on Windows
# or zmqRep.py <port>

if len(sys.argv) < 2:
    print "usage zmqRep.py <bindPort>"
    cmdPromptUtils.waitExit()

# Boilerplate zmq code, create context and socket
ctx = zmq.Context()
sock = ctx.socket(zmq.REP)

# port no from argv to bind to
port = int(sys.argv[1])
print "binding to port %i" % port
sock.bind("tcp://*:%i" % port)

# A Rep socket can only serially process
# requests, recv is called first, then
# a send, and so-on
while True:
    print "Receiving..."
    echoData = sock.recv()
    print "Sending... %s" % echoData
    sock.send(echoData)