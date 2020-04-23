import socket as soc
import threading
import sys
import time
import redis
import signal

def ret(socket, shouldStop):
    start = time.time() 
    while shouldStop:
        try:
            data = socket.recv(4096)
            yield data
        except:
            shouldStop = False
            break
    print("done")
    socket.shutdown(soc.SHUT_RDWR)
    socket.close()

def receive(socket, shouldStop, r):
    provider = ret(socket, shouldStop)
    c = 0
    for data in provider:
        print("{} {}".format(c, len(data)))
        r.publish('radio', data)
        c = c + 1

sock = soc.socket(soc.AF_INET, soc.SOCK_STREAM)
sock.connect(('localhost', 6789))
r = redis.StrictRedis(host='localhost', port=6379, db=0)

receiveThread = threading.Thread(target = receive, args = (sock, True, r))
receiveThread.start()