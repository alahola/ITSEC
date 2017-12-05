import argparse

import ssl
import socket

import sys


class MiddleMan:

    def __init__(self, ident: str, port: int):
        self.adress = (ident, port)
        self.sock = socket.create_connection(self.adress)
        self.ssl_socket = ssl.wrap_socket(sock=self.sock)

    def read(self):
        return self.ssl_socket.read()

    def write(self, m):
        self.ssl_socket.write(m)


def doExercise(ident, port):
    alice = MiddleMan(ident, port);
    eve = MiddleMan(ident, port);

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
            if str(oldm1).find("Uh, a flag:") > 0:
                flag = oldm1
            else:
                flag = oldm2
            break;
    strf = str(flag)
    flag = strf[14:len(strf) - 3]
    write(flag, "flag.txt")


def write(writin: str, filename: str):
    file = open(filename, "r+")
    file.write(writin)
    file.close()

def byteToString(byte: bytes):
    string = str(byte)
    return string[2:len(string)-1]

parser = argparse.ArgumentParser(description='doin man in the middle')
parser.add_argument('--out', type=str, default='')
parser.add_argument('DOMAIN', type=str)
parser.add_argument('PORT', type=int)
args = parser.parse_args()

for m in doExercise(args.DOMAIN, args.PORT):
    print(m)
    #sys.stdout.write(byteToString(m))







