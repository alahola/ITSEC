'''
Created on 06.11.2017

@author: Anna-Liisa
'''
import argparse
import collections



parser = argparse.ArgumentParser(description='Encrypting')
parser.add_argument('out', type=str)
args = parser.parse_args()

if(args.out != None):
    
    alphabet = []
        
    for letter in range(65, 91):
            alphabet.append(chr(letter))
    for letter in range(97,123):
            alphabet.append(chr(letter))
        
    loweralphabet = []  
    for letter in range(97,123):
        loweralphabet.append(chr(letter))
        
    fileM = open(args.out)
    text = fileM.read()    
        
    formatedtext = ''.join([i for i in text if i in alphabet])
        
        
    formatedtext = formatedtext.lower();
        
    
    letterFrequencyOrder = "etaoinsrhldcumfpgwybvkxjqz"
    
    
    
    frequencies = collections.Counter(text)
    
    
def readWordlist(filename: str, wordlen: int):
    file = open(filename)
    line = file.readline()
    index = 1
    chars = {}
    while line != "":
        chars[line[:wordlen]] = float(line[wordlen+3:])
        index += 1
        line = file.readline()
    file.close()
    return chars    
    
    
    
