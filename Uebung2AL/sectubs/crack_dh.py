'''
Created on 10.11.2017

@author: Anna-Liisa
'''
import argparse

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('-g', type=int)
parser.add_argument('-n', type=int)
parser.add_argument('--alice', type=int)
parser.add_argument('--bob', type=int)