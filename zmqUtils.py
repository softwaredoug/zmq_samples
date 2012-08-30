import zmq

def recvAll(sock):
    """ Receive all parts of the envelope"""
    parts = [sock.recv()]
    while sock.getsockopt(zmq.RCVMORE):
        parts.append(sock.recv())
    return parts

def sendAll(sock, parts):
    """ send all parts passed in"""
    if parts:
        for part in parts[:-1]:
            sock.send(part, zmq.SNDMORE)
        sock.send(parts[-1])