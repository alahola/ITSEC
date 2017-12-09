import argparse
from socket import socket, SOCK_RAW, gethostname, IPPROTO_TCP

import struct

parser = argparse.ArgumentParser(description='send packet')
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument('--syn', action='store_true')
group.add_argument('--xmas', action='store_true')
group.add_argument('--fin', action='store_true')
group.add_argument('--null', action='store_true')
parser.add_argument('DOMAIN', type=str)
parser.add_argument('PORT', type=int)
args = parser.parse_args()

def make_ip(proto, srcip, dstip, ident=54321):
    saddr = socket.inet_aton(srcip)
    daddr = socket.inet_aton(dstip)
    ihl_ver = (4 << 4) | 5
    return struct.pack('!BBHHHBBH4s4s' ,
                       ihl_ver, 0, 0, ident, 0, 255, proto, 0, saddr, daddr)

def make_tcp(srcport, dstport, payload, seq=123, ackseq=0,
             fin=False, syn=False, rst=False, psh=False, ack=False, urg=False,
             window=5840):
    offset_res = (5 << 4) | 0
    flags = (fin | (syn << 1) | (rst << 2) |
             (psh <<3) | (ack << 4) | (urg << 5))
    return struct.pack('!HHLLBBHHH',
                       srcport, dstport, seq, ackseq, offset_res,
                       flags, window, 0, 0)

srcip = '127.0.0.1'
srcport = 11001
payload = 'BUUUUUUUTZ\n'

ip = make_ip(IPPROTO_TCP, srcip, gethostname(args.DOMAIN))
tcp = make_tcp(srcport, args.PORT, payload, fin=(args.fin | args.xmas), syn=(True if args.syn | (args.null == False) else False), urg=args.xmas, psh=args.xmas)
packet = ip + tcp + payload

s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_RAW)
s.sendto(packet, (gethostname(args.DOMAIN), 0))
