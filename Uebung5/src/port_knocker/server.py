import argparse

from scapy.sendrecv import sniff

parser = argparse.ArgumentParser(description='monitor')
parser.add_argument('--port', metavar='INT', type=int, required=True)
parser.add_argument('--shared-key', metavar='INT', type=int, required=True)
parser.add_argument('--num-knocks', metavar='INT', type=int, required=True)
args = parser.parse_args()

pkt = sniff(count=0)
print(pkt[0].summary())
