'''
Created on 06.11.2017

@author: Anna-Liisa
'''
import argparse
import collections
import operator
import re



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
    
    
    

"""
    Calculating (subset of the) key that was used to encrypt word with cipher
    :returns dict[alphachar] = key
"""
def getKey(word: str, cipher: str):
    for c in word:
        positions = []
        index = 0
        for cw in word:
            if c == cw:
                positions.append(index)
            index += 1
        b = True
        lastChecked = ""
        for pos in positions:
            if lastChecked == "":
                lastChecked = cipher[pos]
            else:
                b = b & (lastChecked == cipher[pos])
            lastChecked = cipher[pos]
        if b == False:
            return
    key = {}
    index = 0
    for c in word:
        key[c] = cipher[index]
        index += 1
    return key

"""
    find_string specified by the length
    :returns dict[string] = relative frequency
"""
def find_string(cipher: str, length: int):
    freq = {}
    index = 0
    for c in cipher:
        if index + length - 1 < len(cipher) - 1:
            string = cipher[index:index + length]
            try:
                freq[string] += 1
            except KeyError:
                freq[string] = 1
        index += 1
    for key in freq:
        freq[key] = freq[key] / len(cipher)
    return freq


"""
    Running plaintext-attack on given cipher text
    :param pattern regEx-String e.g. "people" - "[a-z][e][a-z]{3}[e]" if you know 'e'
    you should replace e with key['e'], when u r searching in cipher
    :param word u r searching for - e.g. "people
"""
def plainattack(cipher: str, pattern: str, word: str):
    d = {}
    for index in [m.start() for m in re.finditer(pattern, cipher)]:
        try:
            d[cipher[index:index+len(word)]] += 1
        except KeyError:
            d[cipher[index:index+len(word)]] = 1
    d = sorted(d.items(), key=operator.itemgetter(1), reverse=True)
    return d