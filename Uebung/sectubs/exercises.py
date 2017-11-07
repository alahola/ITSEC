# -*- coding: ascii -*-
'''
Created on 06.11.2017

@author: Anna-Liisa
'''
# coding=utf8
import collections
from collections import Counter
from itertools import chain
import mmap

import filecmp
import os
import subprocess
import tempfile
import unittest
from lib2to3.pgen2.tokenize import tokenize as tokenize
import operator
from itertools import product
import itertools
from asyncore import read
from sectubs.mono.break_mono import alphabet, loweralphabet

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
    def justdoit(filepath):
        Exercises01.calcualteProbaleKeys('')
        
        return
        
        alphabet = Exercises01.getAphabet()
        
        loweralphabet = Exercises01.getLowerAlphabet()
        
        
        text = Exercises01.readTextFromFile(r"C:\Users\Anna-Liisa\Documents\Uni\Master\ITSec\workspace\Uebung\sectubs\ex01_mono.ciphertext.txt")
        
        
#         fileM = open(r"C:\Users\Anna-Liisa\Documents\Uni\Master\ITSec\workspace\Uebung\sectubs\ex01_mono.ciphertext.txt")
#         text = fileM.read()
 
        
        formatedtext = ''.join([i for i in text if i in alphabet])
        
        
        formatedtext = formatedtext.lower();
        
        
        
        letterFrequencyOrder = "eatoinsrhldcumfpgwybvkxjqz"

        frequencies = Counter(formatedtext)
        print(formatedtext)


        text = ''.join([i for i in text if i in loweralphabet])
        
        
        sorted_x = sorted(frequencies.items(), key=operator.itemgetter(1), reverse=True) 
        
#         print(sorted_x)
        
#         keywords = itertools.product(loweralphabet, repeat = 3);
        keywords = [''.join(i) for i in itertools.product(loweralphabet, repeat = 4)]
        
        print(keywords)
        
        i = 0
        
        countlist= {}
        fr = 0;
        
        for k in keywords:
            i = 0
            fr = 0;
            if(k in formatedtext):
                for f in formatedtext:
                    if(i < len(formatedtext)-2): 
                        teststring = formatedtext[i] + formatedtext[i+1]+ formatedtext[i+2]
                        if(k == teststring):
                            fr += 1;
                        i += 1;    
            countlist[k] = fr
        
        
        
        print(countlist)    
        
        countlistsorted = sorted(countlist.items(), key=operator.itemgetter(1), reverse=True) 
        
        print(countlistsorted)
        
            
#         if s.find(b'jgt') != -1:
#             print(s.find(b'jgt'))
#             print(s.find(b'mtn'))
#             print('true')


            
        
        key = [None] * 26

        for i in sorted_x:
            print(i)
            
            print(sorted_x.index(i))
            
            
            #ersmalposition und value in letter frequencies
            positionInFrequencyOrder = letterFrequencyOrder[sorted_x.index(i)];
            
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
            
            
        result = Exercises01.encryptThisText(text, key)
        
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
#         fname = Exercises01.tmpfile()
# 
#         with open(fname, 'wb') as f:
#             f.write(b'Exerciseww 01')
#             f.seek(0)
#             
#             
#         print(fname)
        
            


        
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
            

        print(result)
        
        
        
        
ex = Exercises01();
ex.encrypt("b'Exercise'", "abcdefghijklmnopqrstuvwxyz", "mono/mono.py")
ex.justdoit("filepath")
