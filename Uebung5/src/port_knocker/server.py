import argparse
import operator
from _sha256 import sha256
from scapy.all import *


def unlock():
    log("unlocked")


def log(msg: str):
    print(msg)


class server(object):

    def __init__(self, port, key : int, knocks):
        self.port = port
        self.key = key
        self.knocks = knocks

        log("Starting port knocker daemon...")

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
            send(c_packet)
            send(c_packet)
            send(c_packet)
            send(c_packet)
            ports = []
            knock_point = 0

            while knock_point < self.knocks:
                ports.append(self.p(knock_point, c, key))
                knock_point = knock_point + 1

            log("Starting challenge " + str(c) + " with " + packet['IP'].src + " on ports " + str(ports))
            filter = 'tcp and tcp[tcpflags] & (tcp-syn) != 0 and tcp src port ' + str(self.port) + ' and ip host ' + packet['IP'].src
            if len(ports) != 1:
                filter += ' and dst port ('
                first = True
                for p in ports:
                    if first:
                        filter += str(p)
                        first = False
                    else:
                        filter += ' or ' + str(p)
                filter += ')'
            else:
                filter += ' and dst port ' + str(ports[0])
            packets = sniff(count=self.knocks * 2, filter=filter, timeout=5)
            if not (len(packets) >= self.knocks):
                log('Challenge unsuccessful, remaining...')
            else:
                d = {}
                for port in ports:
                    d[port] = 0
                i = 0
                c_ports = ports.copy()
                for packet in packets:
                    tcp = packet["TCP"]
                    if len(ports) != 0:
                        try:
                            if d.get(tcp.dport) == 0:
                                d[tcp.dport] = i
                            ports.remove(tcp.dport)
                        except ValueError:
                            pass
                    i += 1
                sorted_inde = sorted(d.items(), key=operator.itemgetter(1))
                i = 0
                right_seq = True
                for key_val in sorted_inde:
                    if key_val[0] != c_ports[i]:
                        right_seq = False

                if len(ports) == 0 & right_seq:
                    unlock()




    def p(self, i: int, c: int, k: int):
        myString = str((k * c + i))
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
  
