'''
Created on 10.11.2017

@author: Anna-Liisa
'''
import argparse
from sectubs.crack_dh import getPossibleSecretAlice

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('-g', type=int)
parser.add_argument('-n', type=int)
parser.add_argument('--alice', type=int)
parser.add_argument('--bob', type=int)


generator = parser.g;
prime = parser.n;

getPossibleSecretAlice(6, 3, 17);

def getPossibleSecretAlice(alicePublic, generator, prime):
    i =0;
    possibleSecretAlice = []
    while i < 200:
        if(generator^i % prime == alicePublic):
            possibleSecretAlice.append(i)
        i += 1
            
    
    print(possibleSecretAlice) 