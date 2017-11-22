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

def doExercise(ident, port):
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
            yield m1
            yield m2
            eve.write(m1)
            alice.write(m2)
        except ssl.SSLEOFError:
            if oldm1.find("Uh, a flag:"):
                flag = oldm1
            else:
                flag = oldm2
            break;

    yield flag
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
        print(m1)
        print(m2)
        eve.write(m1)
        alice.write(m2)
    except ssl.SSLEOFError:
        flag = oldm1
        break;

print("Flagge: " + str(flag))



