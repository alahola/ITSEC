'''
Created on 06.11.2017

@author: Anna-Liisa
'''
import argparse
from sectubs.mono.analysis import *



parser = argparse.ArgumentParser(description='Encrypting')
parser.add_argument('out', type=str)
args = parser.parse_args()

if(args.out != None):

    fileM = open(args.out)
    text = fileM.read()

    alphabet = []

    for letter in range(65, 91):
        alphabet.append(chr(letter))
    for letter in range(97, 123):
        alphabet.append(chr(letter))

    loweralphabet = []
    for letter in range(97, 123):
        loweralphabet.append(chr(letter))

    formatedtext = ''.join([i for i in text if i in alphabet])

    formatedtext = formatedtext.lower();

    print(decrypt(formatedtext))
