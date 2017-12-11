import argparse
import socket
from struct import pack


def tcp_checksum(msg):
    s = 0
    # loop taking 2 characters at a time
    for i in range(0, len(msg), 2):
        w = msg[i] + (msg[i + 1] << 8)
        s = s + w
    s = (s >> 16) + (s & 0xffff)
    s = s + (s >> 16)
    s = ~s & 0xffff
    return s


parser = argparse.ArgumentParser(description='send packet')
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument('--syn', action='store_true')
group.add_argument('--xmas', action='store_true')
group.add_argument('--fin', action='store_true')
group.add_argument('--null', action='store_true')
parser.add_argument('DOMAIN', type=str)
parser.add_argument('PORT', type=int)
args = parser.parse_args()

# TCP packet
# 2byte
src_port = 1234
dest_port = args.PORT
# 4byte
seq_num = 0
# 4byte
ack_num = 0
# 4it
data_off = (5 << 4) + 0
# 1bit
cwr_flag = False
ece_flag = False
urg_flag = args.xmas
ack_flag = False
psh_flag = args.xmas
rst_flag = False
syn_flag = args.syn
fin_flag = True if args.fin | args.xmas else False

tcp_flags = \
    fin_flag \
    + (syn_flag << 1) \
    + (rst_flag << 2) \
    + (psh_flag << 3) \
    + (ack_flag << 4) \
    + (urg_flag << 5) \
    + (ece_flag << 6) \
    + (cwr_flag << 7)

# 2byte
win = socket.htons(5840)
checksum = 0
urgent_pointer = 0
# 4byte
options = 0

tcp_packet = pack(
    '!HHLLBBHHH',
    src_port,
    dest_port,
    seq_num,
    ack_num,
    data_off,
    tcp_flags,
    win,
    checksum,
    urgent_pointer
)

# TCP-Pseudoheader
# 4byte
src_ip = b'127.0.0.1'
dest_ip = bytes(socket.gethostbyname(args.DOMAIN), 'UTF-8')
# 2byte
prot = socket.IPPROTO_TCP
tcp_len = len(tcp_packet)

pseudo_header = pack(
    '!4s4sBBH',
    src_ip,
    dest_ip,
    0,
    prot,
    tcp_len
)

checksum = tcp_checksum(pseudo_header + tcp_packet)

tcp_packet = pack(
    '!HHLLBBH',
    src_port,
    dest_port,
    seq_num,
    ack_num,
    data_off,
    tcp_flags,
    win
) + pack(
    'H', checksum
) + pack(
    '!H', urgent_pointer
)

s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_RAW)
s.sendto(tcp_packet, (socket.gethostbyname(args.DOMAIN), 0))
