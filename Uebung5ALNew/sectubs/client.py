'''
Created on 11.12.2017

@author: Anna-Liisa
'''
import argparse
import socket
import random
from scapy.layers.inet import IP, TCP, send, sr1
import sys
from logging import Logger

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('--shared-key', type=int)
parser.add_argument('--num-knocks', type=int)
parser.add_argument('--port', type=int)
# parser.add_argument('DOMAIN', type=str)
# parser.add_argument('PORT', type=int)
args = parser.parse_args()

args.port = 1000


# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Connect the socket to the port where the server is listening
# server_address = ('localhost', args.port)
# print('connecting to %s port %s' % server_address)
# sock.connect(server_address)


UDP_IP = "127.0.0.1"
UDP_PORT = 1000
MESSAGE = b'heyjooo'

#Sends UDP to server
sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))

while True:
    #Waits to receive UDP Package with challenge from server 
    data, addr = sock.recvfrom(1024)
    print("received messg:", data)
    
    
    # VARIABLES
    src = UDP_IP
    dst = UDP_IP
    sport = random.randint(1024,65535)
    dport = int(UDP_PORT)
 
    # SYN
    ip=IP(src=src,dst=dst)
    SYN=TCP(sport=sport,dport=dport,flags='S',seq=1000)
    SYNACK=sr1(ip/SYN)
 
    # ACK
    ACK=TCP(sport=sport, dport=dport, flags='A', seq=SYNACK.ack, ack=SYNACK.seq + 1)
    send(ip/ACK)



    def send_syn(self):
        Logger.debug("SND: SYN")
        self.l4[TCP].flags = "S"
        self.seq_next = self.l4[TCP].seq + 1
        response = self._sr1(self.l4)
        self.l4[TCP].seq += 1
        return self.handle_recv(response)
    
    

# try:
#     
#     # Send data
#     message = 'This is the message.  It will be repeated.'
#     print('sending "%s"' % message)
#     sock.sendall(b'message')
# 
#     # Look for the response
#     amount_received = 0
#     amount_expected = len(message)
#     
#     while amount_received < amount_expected:
#         data = sock.recv(16)
#         amount_received += len(data)
#         print('received "%s"' % data)
# 
# finally:
#     print('closing socket')
#     sock.close()

