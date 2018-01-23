import argparse
from _sha256 import sha256
from time import sleep

from scapy.all import *



class client(object):

    def __init__(self, host, port, key: int, knocks):
        self.key = key
        self.knocks = knocks
        self.host = host
        self.port = port
        
        c_packet = IP(
            dst=self.host
        ) / UDP(
            sport=self.port,
            dport=self.port
        )
        send(c_packet)

        filter = 'udp and port ' + str(self.port) + ' and host ' + str(self.host)
        packets = sniff(count=1, filter=filter)
        packet = packets[0]

        udp = packet["UDP"]
        challenge = udp.payload
        print("Client received challenge: ", challenge)

        knock_point = 0

        ports = []

        c = self.byteToString(challenge)
        cInt = int(c)
        while knock_point < self.knocks:
            ports.append(self.p(knock_point, cInt, key))
            knock_point = knock_point + 1

        sleep(1)
        for port in ports:
            print("Sending tcp to ", port)
            tcp_packet = IP(
                dst=host
            ) / TCP(
                sport=self.port,
                dport=port,
                flags='S'
            )
            send(tcp_packet)

            
    def byteToString(self, byte: bytes):
        string = str(byte)
        return string[2:len(string)-1] 

    def p(self, i: int, c: int, k: int):
        myString = str((k * c + i))
        encodedString = myString.encode()
        sharesult = sha256(encodedString)
        val_hex = sharesult.hexdigest()
        val_int = int(val_hex, 16)
        return 1024 + (val_int % 28657)


parser = argparse.ArgumentParser(description='monitor')
parser.add_argument('--shared-key', metavar='INT', type=int, required=True)
parser.add_argument('--num-knocks', metavar='INT', type=int, required=True)
parser.add_argument('host', metavar='IP/DOMAIN', type=str)
parser.add_argument('port', metavar='PORT', type=int)
args = parser.parse_args()

s = client(socket.gethostbyname(args.host), args.port, args.shared_key, args.num_knocks)
