'''
Created on 08.12.2017

@author: Anna-Liisa
'''
import argparse
import socket
import sys
import random
from scapy.layers.inet import IP, TCP, send, sr1
from logging import Logger

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('--port', type=int)
parser.add_argument('--shared-key', type=int)
parser.add_argument('--num-knocks', type=int)
args = parser.parse_args()


UDP_IP = "127.0.0.1"
UDP_PORT = 1000
MESSAGE = "heyjooo"



# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

args.port = 1000

# Bind the socket to the port
# server_address = ('localhost', args.port)
# print('starting up on %s port %s' % server_address)
#print >>sys.stderr, 'starting up on %s port %s' % server_address
sock.bind((UDP_IP, UDP_PORT))

i=0
while True:
    #waits to receive UDP Package
    data, addr = sock.recvfrom(1024)
    print("received messg:", data)
    
    try:
        
        if(i<1):
            # on receive of UDP package server answers with another UDP package including a numerical challange
            sock.sendto(b'1000', addr)
            print("Sended something")
            i = 1
            
            while True: 
         
                #waiting for a specific number of TCP packages
                packet = IP(dst=addr)/TCP(UDP_PORT)
                unans, ans = sr1(packet)
                print(ans)
                
                
            
        
            
        
    finally:
        pass
    
    
    
    def handle_recv(self, pkt):
        if pkt and pkt.haslayer(IP) and pkt.haslayer(TCP):
            if pkt[TCP].flags & 0x3f == 0x12:   # SYN+ACK
                Logger.debug("RCV: SYN+ACK")
                return self.send_synack_ack(pkt)
            elif  pkt[TCP].flags & 4 != 0:      # RST
                Logger.debug("RCV: RST")
                raise Exception("RST")
            elif pkt[TCP].flags & 0x1 == 1:     # FIN
                Logger.debug("RCV: FIN")
                return self.send_finack(pkt)
            elif pkt[TCP].flags & 0x3f == 0x10: # FIN+ACK
                Logger.debug("RCV: FIN+ACK")
                return self.send_ack(pkt)

        Logger.debug("RCV: %s"%repr(pkt))
        return None
    
    

# # Listen for incoming connections
# sock.listen(1)
# 
# while True:
#     # Wait for a connection
#     print('waiting for a connection')
#     connection, client_address = sock.accept()
#      
#     try:
#         print('connection from' , client_address)
# 
#     # Receive the data in small chunks and retransmit it
#         while True:
#             data = connection.recv(16)
#             print('received "%s"' % data)
#             if data:
#                 print('sending data back to the client')
#                 connection.sendall(data)
#             else:
#                 print('no more data from', client_address)
# 
#     finally:
#     # Clean up the connection
#         connection.close()