import zmq
import sys
import itertools

ctx = zmq.Context()
sock = ctx.socket(zmq.DEALER)

for port in sys.argv[1:-1]:
    print "Connecting to port %i" % int(port)
    sock.connect("tcp://localhost:%i" % int(port))
echoText = sys.argv[-1]

class TimeoutError(Exception):
    pass

def timeoutRcv(sock,timeoutMsec):
    """ Timeout on work"""
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
    thisEchoText = echoText + ("(%i)" % i)
    sock.send(thisEchoText)
    print "Receiving..."
    try:
        echoTextBack = timeoutRcv(sock, timeoutMsec=1000)
        print "> %s" % echoTextBack
    except TimeoutError:
        print "! %s TimedOut!" % thisEchoText
        
while True:
    pass