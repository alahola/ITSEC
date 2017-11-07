# -*- coding: ascii -*-
'''
Created on 06.11.2017

@author: Anna-Liisa
'''
# coding=utf8
import collections
from collections import Counter
from itertools import chain

import os
import tempfile
import operator
import itertools

class Exercises01(object):
   
    MY_DIR = os.path.dirname(os.path.abspath(__file__))
    
    @staticmethod
    def getAphabet():
        alphabet = []
        
        for letter in range(65, 91):
            alphabet.append(chr(letter))
        for letter in range(97,123):
            alphabet.append(chr(letter))
        return alphabet
        

    @staticmethod
    def getLowerAlphabet():
        loweralphabet = []  
        for letter in range(97,123):
            loweralphabet.append(chr(letter))
            
        return loweralphabet;
    
    @staticmethod
    def readTextFromFile(path):
         
        fileM = open(path)
        text = fileM.read() 
        return text  
    
    @staticmethod
    def getCharacterFrequenciesInText(alphabet, size, text):
        keywords = [''.join(i) for i in itertools.product(alphabet, repeat = size)]

        i = 0
        
        countlist= {}
        fr = 0;
        
        for k in keywords:
            i = 0
            fr = 0;
            if(k in text):
                for f in text:
                    if(i < len(text)-2): 
                        teststring = text[i] + text[i+1]+ text[i+2]
                        if(k == teststring):
                            fr += 1;
                        i += 1;    
            countlist[k] = fr
        
        countlistsorted = sorted(countlist.items(), key=operator.itemgetter(1), reverse=True) 
        
        print(countlistsorted)
        return countlistsorted
    
    @staticmethod
    def formatText(text, alphabet):
        formatedtext = ''.join([i for i in text if i in alphabet])
        
        
        formatedtext = formatedtext.lower();
        return formatedtext
    
    
    @staticmethod
    def getInternetLetterFreqOder():
        return "eatoinsrhldcumfpgwybvkxjqz"
        
    @staticmethod
    def justdoit(filepath):
        Exercises01.calcualteProbaleKeys('')

        alphabet = Exercises01.getAphabet()
        
        loweralphabet = Exercises01.getLowerAlphabet()
        
        
        text = Exercises01.readTextFromFile(r"C:\Users\Anna-Liisa\Documents\Uni\Master\ITSec\workspace\Uebung\sectubs\ex01_mono.ciphertext.txt")
        
 
        formatedtext = Exercises01.formatText(text, alphabet)
 
        letterFreqInternet = Exercises01.getInternetLetterFreqOder()


        letterFreqCipherText = Counter(formatedtext)

        
        letterFreqCipherText = sorted(letterFreqCipherText.items(), key=operator.itemgetter(1), reverse=True) 
        
        
        letterRowFreqCipherText = Exercises01.getCharacterFrequenciesInText(loweralphabet, 3, formatedtext)
        
        print(letterRowFreqCipherText)
    
        
        key = [None] * 26

        for i in letterFreqCipherText:
        
            
            positionInFrequencyOrder = letterFreqInternet[letterFreqCipherText.index(i)];
            
            positionInAlphabet = loweralphabet.index(positionInFrequencyOrder);
            
            key[positionInAlphabet] = i[0]
        
        alp = []
        for a in loweralphabet:
            alp.append(a);
        print(alp)    
        print(key)
    

        key[loweralphabet.index('h')] = 'g';
        key[loweralphabet.index('r')] = 'a';
        
#         key[loweralphabet.index('e')] = 't';
#         key[loweralphabet.index('r')] = 't';

        key[loweralphabet.index('a')] = 'o';
        key[loweralphabet.index('o')] = 'p';
        
        key[loweralphabet.index('o')] = 'r';
        key[loweralphabet.index('n')] = 'p';
        
        key[loweralphabet.index('d')] = 'z';
        key[loweralphabet.index('f')] = 'd';
        
#         key
            
            
        result = Exercises01.encryptThisText(formatedtext, key)
        
        print(result)
        
#         c = Counter()
# 
#         for ch in filter(str.isalpha, chain.from_iterable('the')):
#             c[result + ch] += 1
#             result = ch
#             print(c)
      
   
   
    @staticmethod
    def encryptThisText(text, key):
        print(text)
        
        print("d")



        loweralphabet = []  
        for letter in range(97,123):
            loweralphabet.append(chr(letter))
            
        result = ""

        for t in text:
            position = key.index(t)
            result = result + loweralphabet[position]
            
        return result
        
    @staticmethod
    def calcualteProbaleKeys(pathLetterFrequencyInternet):
            intfreqletters = Exercises01.readWordlist(r'C:\Users\Anna-Liisa\Documents\Uni\Master\ITSec\workspace\Uebung\sectubs\monograms-english', 1)
            
            changes1 = [''.join(i) for i in itertools.product("ntioa", repeat = 5)]
             
            print(changes1)
            print(len(changes1))
            
            print(intfreqletters)
            
            for l in intfreqletters:
                print(l)
           
            letterFrequencyOrder = "eatoinsrhldcumfpgwybvkxjqz"


    @staticmethod
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
        charssorted = sorted(chars.items(), key=operator.itemgetter(1), reverse=True) 
        
        return charssorted          



    @staticmethod
    def tmpfile():
        fd, fname = tempfile.mkstemp(dir=Exercises01.MY_DIR)
        print(fname)
        os.close(fd)
        return fname 
    
    @staticmethod
    def encrypt(text, key, path):

        
        fileM = open(r"C:\Users\Anna-Liisa\Documents\Uni\Master\ITSec\workspace\Uebung\sectubs\tmp_qrdy9gp")
        text = fileM.read()
        
        
        
        alphabet = []
        
        for letter in range(65, 91):
            alphabet.append(chr(letter))
        for letter in range(97,123):
            alphabet.append(chr(letter))
        
        loweralphabet = []  
        for letter in range(97,123):
            loweralphabet.append(chr(letter))
        
        formatedtext = ''.join([i for i in text if i in alphabet])
        
        
        formatedtext = formatedtext.lower();
        
   
        
 
 
        result = ""

        for t in formatedtext:
            position = loweralphabet.index(t)
            result = result + key[position]
        
        
        
ex = Exercises01();
ex.encrypt("b'Exercise'", "abcdefghijklmnopqrstuvwxyz", "mono/mono.py")
ex.justdoit("filepath")
