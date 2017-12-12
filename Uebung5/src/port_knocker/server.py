import argparse
import random
from _sha256 import sha256
from _thread import start_new_thread

from scapy.layers.inet import IP, UDP
from scapy.sendrecv import sniff, send, sendp


class server(object):

    def __init__(self, port, key, knocks):
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
            ) / bytes(c)
            sendp(c_packet)
            ports = []
            for i in range(0, knocks - 1):
                ports.append(self.p(i, c))
            start_new_thread(self.observeKnocks(packet['IP'].src), ports)

    def observeKnocks(self, src: str, ports: list):
        print("Starting challenge with " + src + " on ports " + str(ports))
        filter = 'tcp and tcp[tcpflags] & (tcp-syn) != 0 and ip host ' + src
        if len(list) != 1:
            filter += ' and dst port ('
            first = True
            for port in list:
                if first:
                    filter += port
                else:
                    filter += ' or ' + port
            filter += ')'
        else:
            filter += ' and dst port ' + list[0]
        packets = sniff(count=self.knocks, filter=filter)
        print('unlocked')

    def p(self, i: int, c: int):
        return 1024 + (sha256(self.key * c + i) % 28657)


parser = argparse.ArgumentParser(description='monitor')
parser.add_argument('--port', metavar='INT', type=int, required=True)
parser.add_argument('--shared-key', metavar='INT', type=int, required=True)
parser.add_argument('--num-knocks', metavar='INT', type=int, required=True)
args = parser.parse_args()

s = server(args.port, args.shared_key, args.num_knocks)
