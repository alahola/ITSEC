'''
Created on Dec 6, 2017

@author: y0066709
'''
import argparse

import ssl
import socket

import sys


class MiddleMan:

    def __init__(self, ident: str, port: int):
        self.adress = (ident, port)
        self.sock = socket.create_connection(self.adress)
        self.ssl_socket = ssl.wrap_socket(sock=self.sock)
        self.ch = 0
        self.speech = [
            "Nono. UNTIL I come and get him.\n",
            "No, no, no... You stay in the room, and make sure he does not leave.\n",
            "Nono. Leaving the room.",
            "Alright?",
            "Look it's quite simple. You just stay here, and make sure he doesn't leave the room Alright?",
            "no No nono. You just keep him in here and make sure h..."
        ]

    def weird_proto(self):
        m = self.read()
        x = stringToInt(m)
        yield m
        yield self.challenge()
        yield self.read()
        yield self.response(x)
        #
        yield self.write("Guards, make sure the prince doesn't leave this room until I come and get him.\\n")
        yield self.read()
        
        #--------------------------
        m = self.read()
        x = stringToInt(m)
        yield m
        yield self.response(x)
        yield self.challenge()
        yield self.read()
        
        yield self.write(self.speech[0])
        yield self.read()
        #----------------------
        
        m = self.read()
        x = stringToInt(m)
        yield m
        yield self.response(x)
        
        yield self.challenge()
        yield self.read()

 


        yield self.write(self.speech[1])
        yield self.read()


        
        
      

    def sub_proto(self):
        m = self.read()
        x = stringToInt(m)
        yield m
        yield self.response(x)
        yield self.challenge()
        yield self.read()
#         yield self.read()

    def read(self):
        m = self.ssl_socket.read()
        return byteToString(m)

    def write(self, m: str):
        self.ssl_socket.write(bytearray(m, 'UTF-8'))
        return m

    def response(self, x: int):
        r = (-9 + 2 * x + x // 3) % 10000
        if r < 10:
            return self.write("000" + str(r) + "\n")
        if r < 100:
            return self.write("00" + str(r) + "\n")
        if r < 1000:
            return self.write("0" + str(r) + "\n")
        else:
            return self.write(str(r) + "\n")

    def challenge(self):
        self.ch += 1
        return self.write(str(self.ch) + '000\n')


def write(writin: str, filename: str):
    file = open(filename, "r+")
    file.write(writin)
    file.close()

def byteToString(byte: bytes):
    string = str(byte)
    return string[2:len(string)-1]

def stringToInt (s: str):
    return int(s[:len(s)-2])

def doExercise(ident, port):
    alice = MiddleMan(ident, port)
    yield alice.read()



parser = argparse.ArgumentParser(description='doin man in the middle')
parser.add_argument('--out', type=str, default='')
parser.add_argument('DOMAIN', type=str)
parser.add_argument('PORT', type=int)
args = parser.parse_args()



alice = MiddleMan(args.DOMAIN, args.PORT)

for m in alice.weird_proto():
    print(m)