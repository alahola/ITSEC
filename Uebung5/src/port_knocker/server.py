import argparse
import random
from _sha256 import sha256
from _thread import start_new_thread
from threading import Thread

from scapy.layers.inet import IP, UDP, Raw, TCP
from scapy.sendrecv import sniff, send, sendp, sr1


class server(object):

    def __init__(self, port, key : int, knocks):
        self.port = port
        self.key = key
        self.knocks = knocks
        while True:
            packets = sniff(count=1, filter='udp and port ' + str(port))
            packet = packets[0]
            c = random.randint(0, 100)
            c_packet = IP(
                dst=packet['IP'].src,
                src=packet['IP'].dst
            ) / UDP(
                sport=port,
                dport=packet['UDP'].sport
            ) / str(c)
            print(str(c_packet))
            send(c_packet)
            print("challenge send: ", c)
            ports = []
            knock_point = 0
                
            while knock_point < self.knocks:
                ports.append(self.p(knock_point, c, key))
                knock_point = knock_point+1

            portObserver = Thread(
                target = self.observeKnocks,
                args=(packet['IP'].src, ports)
            )


    def observeKnocks(self, src: str, ports: list):
        print("Starting challenge with " + src + " on ports " + str(ports))
        filter = 'tcp and tcp[tcpflags] & (tcp-syn) != 0 and ip host ' + src
        if len(ports) != 1:
            filter += ' and dst port ('
            first = True
            for p in ports:
                if first:
                    filter += str(p)
                else:
                    filter += ' or ' + str(p)
            filter += ')'
        else:
            filter += ' and dst port ' + str(ports[0])
        packets = sniff(count=self.knocks, filter=filter)
        print('unlocked')

    def p(self, i: int, c: int, k: int):
        myString = str((k * c + i))
        print(myString)
        encodedString = myString.encode()
        sharesult = sha256(encodedString)
        val_hex = sharesult.hexdigest()
        val_int = int(val_hex, 16)
        return 1024 + (val_int % 28657)


parser = argparse.ArgumentParser(description='monitor')
parser.add_argument('--port', metavar='INT', type=int, required=True)
parser.add_argument('--shared-key', metavar='INT', type=int, required=True)
parser.add_argument('--num-knocks', metavar='INT', type=int, required=True)
args = parser.parse_args()

s = server(args.port, args.shared_key, args.num_knocks)
  
