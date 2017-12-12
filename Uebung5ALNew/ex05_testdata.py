'''
@author: Christian Wressnegger
'''


SEND_PACKET = b'''
usage: send_packet.py [-h] (--syn | --xmas | --fin | --null) IP/DOMAIN PORT
send_packet.py: error: the following arguments are required: IP/DOMAIN, PORT
'''

CLIENT = b'''
usage: client.py [-h] --shared-key INT --num-knocks INT IP/DOMAIN PORT
client.py: error: the following arguments are required: IP/DOMAIN, PORT
'''

SERVER = b'''
usage: server.py [-h] --port INT --shared-key INT --num-knocks INT
server.py: error: the following arguments are required: --port, --shared-key, --num-knocks
'''

SYNOPSIS = {
    "send_packet": SEND_PACKET,
    "client": CLIENT,
    "server": SERVER
}


def verify_synopsis(x, s):
    try:
        return (SYNOPSIS[x].strip() in s)
    except KeyError:
        return False
