import argparse
from _sha256 import sha256

from scapy.layers.inet import IP, UDP, send, sniff, TCP



class client(object):

    def __init__(self, host, port, key: int, knocks):
        self.key = key
        self.knocks = knocks
        self.host = host
        self.port = port
        
        c_packet = IP(
            dst=host
        ) / UDP(
            dport=port
        )
        send(c_packet)
        
        while True:
            packets = sniff(count=1, filter='udp and port ' + str(port))
            print(packets)
            packet = packets[0]
            
#             self.getLayersOfPacket(packet)
            
            if packet and packet.haslayer(UDP):
                udp = packet["UDP"]
                challenge = udp.payload
                print("Client received following challenge: " , challenge)
                
                knock_point = 0;
                
                ports = [] 
                
                c = self.byteToString(challenge)
                cInt = int(c)
                while knock_point < self.knocks:
                    
                    ports.append(self.p(knock_point, cInt, key))
                    knock_point = knock_point+1
                
                for port in ports:
                    tcp_packet = IP(
                    dst=host
                    ) / TCP(
                    sport=port,
                    dport=port
                    )
                    
                    send(tcp_packet) 
                
        

    def getLayersOfPacket(self, packet):
        layers = []
        counter = 0
        
        while packet.getlayer(counter) != None:
            layer = packet.getlayer(counter)
            if (layer != None):
                print(layer.name)
                layers.append(layer.name)
            else:
                break
            counter += 1


        udp = packet["UDP"]
        print(udp.payload)
        print("Layers are:\t\t",layers)
    
            
    def byteToString(self, byte: bytes):
        string = str(byte)
        return string[2:len(string)-1] 

    def p(self, i: int, c: int, k: int):
        myString = str((k * c + i))
        print(myString)
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

s = client(args.host, args.port, args.shared_key, args.num_knocks)
