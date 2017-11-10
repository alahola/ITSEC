'''
Created on 10.11.2017

@author: Anna-Liisa
'''
import argparse
import sys
from dhanalysis import solveDH

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('-g', type=int)
parser.add_argument('-n', type=int)
parser.add_argument('--alice', type=int)
parser.add_argument('--bob', type=int)
args = parser.parse_args()


generator = args.g;
prime = args.n;

result = solveDH(args.alice, args.bob, generator, prime)
sys.stdout.write(str(result))




