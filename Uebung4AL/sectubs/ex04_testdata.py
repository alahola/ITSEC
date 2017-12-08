'''
@author: Christian Wressnegger
'''


def verify_msgs(s):
    return (len(s) > 1024)


def verify_flag(s):
    return (len(s) == 64)
