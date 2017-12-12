import argparse
from _sha256 import sha256

from scapy.layers.inet import IP, UDP
from scapy.sendrecv import sr1


class client(object):

    def __init__(self, host, port, key, knocks):
        self.key = key
        self.knocks = knocks
        self.host = host
        self.port = port

        packet = IP(
            dst=host
        ) / UDP(
            dport=port
        )
        ans = sr1(packet)



    def p(self, i: int, c: int):
        return 1024 + (sha256(self.key * c + i) % 28657)



parser = argparse.ArgumentParser(description='monitor')
parser.add_argument('--shared-key', metavar='INT', type=int, required=True)
parser.add_argument('--num-knocks', metavar='INT', type=int, required=True)
parser.add_argument('host', metavar='IP/DOMAIN', type=str)
parser.add_argument('port', metavar='PORT', type=int)
args = parser.parse_args()
