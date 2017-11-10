'''
Created on 10.11.2017

@author: Anna-Liisa
'''

class MyClass(object):
    '''
    classdocs
    '''

    @staticmethod
    def getPossibleSecretNumbers(publicNumber, generator, prime):
        i =0;
        possibleSecretAlice = []
        while i < 10000:
            if(((generator**i) % prime) == publicNumber):
                possibleSecretAlice.append(i)
            i += 1
            
    
        return possibleSecretAlice
    
    @staticmethod
    def checkAllCombinations(possibleAlice, possibleBob, alicePublic, bobPublic, prime):
        i = 0;
        key = 0
        for a in possibleAlice:
            for b in possibleBob:
                if((bobPublic**a % prime) == (alicePublic**b %prime)):
                    i = i+1;
                    key = (bobPublic**a % prime)
                    return key
                
    @staticmethod
    def testtest(n):
        i = 1
        j = n
        result = []
#         result.append(result1)
#         result.append(result2)
        f = n/2
        while i < f:
            while j > 1:
                if(i * j == n):
                    r = (i, j)
                    result.append(r)
                    return
            
                
         
alicePublic = 929
bibPublic = 626   
ex = MyClass();
# possibelSecretAlice= ex.getPossibleSecretNumbers(alicePublic, 10, 1783);
# possibleSecretBob = ex.getPossibleSecretNumbers(bibPublic, 10, 1783);
# result = ex.checkAllCombinations(possibelSecretAlice, possibleSecretBob, alicePublic, bibPublic, 1783)
# print(result)
# print(solveDH(alicePublic, bibPublic, 10, 1783))
ex.testtest(67063)

