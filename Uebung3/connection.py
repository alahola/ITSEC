import ssl
from ssl import SSLContext
import socket

class MiddleMan:

    def __init__(self):
        self.adress = ('weird.sec.tu-bs.de', 3333)
        self.sock = socket.create_connection(self.adress)
        self.ssl_socket = ssl.wrap_socket(sock=self.sock)

    def read(self):
        return self.ssl_socket.read()

    def write(self, m):
        self.ssl_socket.write(m)


alice = MiddleMan();
eve = MiddleMan();

oldm1 = ""
oldm2 = ""
m1 = ""
m2 = ""
while True:
    oldm1 = m1
    oldm2 = m2
    try:
        m1 = alice.read()
        m2 = eve.read()
        eve.write(m1)
        alice.write(m2)
    except ssl.SSLEOFError:
        flag = oldm1
        break;

print("Flagge: " + str(flag))



