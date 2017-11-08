import operator

import itertools
import re

from sectubs.mono import myio, mono


def decrypt(cipher: str):
    key = {}
    for i in range(97, 97 + 26):
        key[chr(i)] = None
    cfreq = find_string(cipher, 1)
    # All chars in?
    for c in "abcdefghijklmnopqrstuvwxyz":
        if c not in cfreq.keys():
            cfreq[c] = 0
    monograms = sorted(cfreq.items(), key=operator.itemgetter(1), reverse=True)
    bigrams = sorted(find_string(cipher, 2).items(), key=operator.itemgetter(1), reverse=True)
    trigrams = sorted(find_string(cipher, 3).items(), key=operator.itemgetter(1), reverse=True)
    quadgrams = sorted(find_string(cipher, 4).items(), key=operator.itemgetter(1), reverse=True)

    # Checking monograms v1
    monos = sorted(myio.readWordlist("freq", 1).items(), key=operator.itemgetter(1), reverse=True)
    dist = calcDistances(monos, monograms)
    sum = checkDistribution(monograms, monos)
    if sum < 0.01:
        # distribution is correct
        res = ""
        for key in dist:
            res += key[1]
        return res

    # Oke its not the plaintext monogram distribution
    monos = sorted(myio.readWordlist("monograms-english", 1).items(), key=operator.itemgetter(1), reverse=True)
    sumMono = checkDistribution(monograms, monos)
    bigr = sorted(myio.readWordlist("bigrams-english", 2).items(), key=operator.itemgetter(1), reverse=True)
    sumBi = checkDistribution(bigrams, bigr)
    trigr = sorted(myio.readWordlist("trigrams-english", 3).items(), key=operator.itemgetter(1), reverse=True)
    sumTri = checkDistribution(trigrams, trigr)
    quadri = sorted(myio.readWordlist("quadrigrams-english", 4).items(), key=operator.itemgetter(1), reverse=True)
    sumQuad = checkDistribution(quadgrams, quadri)

    dist = calcDistances(monos, monograms)
    res = ""
    for key in dist:
        res += key[1]
    return res


def checkDistribution(monocipher, monoreal):
    dist = calcDistances(monoreal, monocipher)
    sum = 0
    for key in dist:
        sum += dist[key]
    return sum


def calcDistances(l1, l2):
    res = {}
    index = 0
    for value in l1:
        res[(value[0], l2[index][0])] = abs(value[1] - l2[index][1])
        index += 1
    return res


"""
    Reading wordlist from raw resource
"""


def readWordlist(filename: str, wordlen: int):
    file = open(filename)
    line = file.readline()
    index = 1
    chars = {}
    while line != "":
        chars[line[:wordlen]] = float(line[wordlen + 3:])
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
            d[cipher[index:index + len(word)]] += 1
        except KeyError:
            d[cipher[index:index + len(word)]] = 1
    d = sorted(d.items(), key=operator.itemgetter(1), reverse=True)
    return d


"""
    Bruteforcing Mono
    Keyspace is significant large better do not do this
"""


def bruteforceMono(cipher: str, subkey: dict):
    alpha = "abcdefghijklmnopqrstuvwxyz"
    print(subkey)
    alpha1 = ""
    alpha2 = ""
    for c in alpha:
        if c not in subkey.keys():
            alpha1 += c
        if c not in subkey.values():
            alpha2 += c

    maxscore = 0
    keyMaxscore = ""
    key = subkey
    for per in itertools.permutations(alpha2):
        index = 0
        for c in alpha1:
            key[c] = per[index]
            index += 1
        index = 0
        test = True
        for c in keyString(key):
            if c == alpha[index]:
                test = False
                break
        if test:
            score = scoreKey(cipher, keyString(key))
        else:
            score = 0
        if score > maxscore:
            maxscore = score
            keyMaxscore = keyString(key)
            print("New score: " + str(maxscore))
            print("New key: " + str(keyMaxscore))
    print("Max score: " + maxscore)
    print("Key: " + keyMaxscore)


def scoreKey(cipher: str, key: str):
    plain = mono.decrypt(cipher, key)
    return scorePlain(plain)


def scorePlain(plain: str):
    score = 0
    for word in myio.lineGenerator("100commons"):
        if plain.find(word) >= 0:
            score += 1
    return score


def keyString(key: dict):
    alpha = "abcdefghijklmnopqrstuvwxyz"
    ret = ""
    for c in alpha:
        ret += key[c]
    return ret
