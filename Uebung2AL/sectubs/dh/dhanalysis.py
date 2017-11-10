'''
Created on 10.11.2017

@author: Anna-Liisa
'''
def getPossibleSecretNumbers(publicNumber, generator, prime, testFrom, testTo):
    i = testFrom;
    possibleSecretAlice = []
    while i < testTo:
        if(((generator**i) % prime) == publicNumber):
            possibleSecretAlice.append(i)
        i += 1

    return possibleSecretAlice


def checkAllCombinations(possibleAlice, possibleBob, alicePublic, bobPublic, prime):
    i = 0;
    key = 0
    for a in possibleAlice:
        for b in possibleBob:
            if((bobPublic**a % prime) == (alicePublic**b %prime)):
                i = i+1;
                key = (bobPublic**a % prime)
                return key

def solveDH(alicePublic, bobPublic, generator, prime):
    testFrom = 0;
    testTo = 10000;
    result = None
    while result == None:
    
        possibelSecretAlice= getPossibleSecretNumbers(alicePublic, generator, prime, testFrom, testTo);
        possibleSecretBob = getPossibleSecretNumbers(bobPublic, generator, prime, testFrom, testTo);
        result = checkAllCombinations(possibelSecretAlice, possibleSecretBob, alicePublic, bobPublic, prime);
        testFrom = testTo;
        testTo = testTo*10

    return result    
           
