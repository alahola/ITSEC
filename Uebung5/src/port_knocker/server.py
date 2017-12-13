import argparse
import random
from _sha256 import sha256
from _thread import start_new_thread

from scapy.layers.inet import IP, UDP, Raw, TCP
from scapy.sendrecv import sniff, send, sendp, sr1


class server(object):

    def __init__(self, port, key : int, knocks):
        self.port = port
        self.key = key
        self.knocks = knocks
        while True:
            
            packets = sniff(count=1, filter='udp and port ' + str(port))
            print(packets)
            packet = packets[0]
            if packet and packet.haslayer(UDP):
                print("Is UDP")
                c = random.randint(0, 100)
                print("this ist random c : ", c)
                c_packet = IP(
                    dst=packet['IP'].src,
                    src=packet['IP'].dst
                ) / UDP(
                    sport=port,
                    dport=packet['UDP'].sport
                ) / str(c)
                send(c_packet)
                ports = []
                
                knock_point = 0;
                
                
                
                while knock_point < self.knocks:
                    
                    ports.append(self.p(knock_point, c, key))
                    knock_point = knock_point+1
                
                
                while True:
                    packets = sniff(count=self.knocks, filter='udp and port')
#                     packets = sniff(count=1, filter='udp and port ' + str(port))
                    print(packets)
                    if len(packets) == self.knocks:
                        knock_point = 0
                        isValidKnock = False
                        for packet in packets:
                            if packet and packet.haslayer(TCP):
                                tcp = packet["TCP"]
                                dport = tcp.dport
                                print("Current port" , dport)
                                
                                print("Current port in list", ports[knock_point])
                                if(dport == ports[knock_point]):
                                    isValidKnock = True
                                else:
                                    isValidKnock = False
                                    break
                                knock_point = knock_point+1
                                
                        
                        if isValidKnock == True:
                            print("unlocked")
                            
                            
                            
                        break;
                    
            break;
                        
                                
                            
                            
                            
                            
                            
                        
                    
                    
                
                
#                 for i in range(0, knocks):
#                     ports.append(self.p(i, c))
#                 start_new_thread(self.observeKnocks(packet['IP'].src , ports))

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
  
