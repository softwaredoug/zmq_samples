import zmq
import signal
import sys

interrupted = False

def signal_handler(signum, frame):
    global interrupted
    print "INTERRUPTED"
    interrupted = True

signal.signal(signal.SIGINT, signal_handler)


def recvAll(sock):
    """ Receive all parts of the envelope"""
    parts = [sock.recv()]
    while sock.getsockopt(zmq.RCVMORE):
        parts.append(sock.recv())
    return tuple(parts)
    
def sendAll(sock, parts):
    """ send all parts passed in"""
    if parts:
        for part in parts[:-1]:
            sock.send(part, zmq.SNDMORE)
        sock.send(parts[-1])
        
context = zmq.Context()

port = int(sys.argv[1])

frontend = context.socket(zmq.ROUTER)
frontend.bind("tcp://*:%i" % port)

poller = zmq.Poller()
poller.register(frontend, zmq.POLLIN)        

allParts = ()

while not interrupted:
    print "Polling..."
    socks = dict(poller.poll(timeout=5000))
    if frontend in socks:
        if socks[frontend] == zmq.POLLIN:
            allParts = recvAll(frontend)
            print "Got %s" % repr(allParts)
            sendAll(frontend, allParts)
frontend.close()
interrupted = False
print "Last work was %s" % repr(allParts)
while not interrupted:
    pass
    