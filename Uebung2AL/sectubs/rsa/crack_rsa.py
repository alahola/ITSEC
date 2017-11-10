'''
Created on 10.11.2017

@author: Anna-Liisa
'''
import argparse

import sys

from rsa_methods import getPlain

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('-e', type=int)
parser.add_argument('-n', type=int)
parser.add_argument('--ciphertext', type=int)
args = parser.parse_args()

sys.stdout.write(str(getPlain(args.e, args.n, args.ciphertext)))