# -*- coding: ascii -*-
import argparse


parser = argparse.ArgumentParser(description='Process some integers.')
# parser.add_argument('integers', metavar='N', type=int, nargs='+',
#                     help='an integer for the accumulator')
# parser.add_argument('--sum', dest='accumulate', action='store_const',
#                     const=sum, default=max,
#                     help='sum the integers (default: find the max)')

group = parser.add_mutually_exclusive_group(required=True)
group.add_argument('--encrypt', type=str)
group.add_argument('--decrypt', type=str)


parser.add_argument('out', type=str)
args = parser.parse_args()



if(args.encrypt != None):

        fileM = open(args.out)
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
            result = result + args.encrypt[position]
            
        print(result)
        
if(args.decrypt != None):
        
        fileM = open(args.out)
        text = fileM.read()


        loweralphabet = []  
        for letter in range(97,123):
            loweralphabet.append(chr(letter))
            
        result = ""

        for t in text:
            position = args.decrypt.index(t)
            result = result + loweralphabet[position]
            
        print(result)
        
    
