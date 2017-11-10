"""
    Creates a list containing the runningkey-values of a key, for example 'abd' returns [0,1,3]
    :param key: The key
    :return: a list containing the running key values
"""
def getRunningkeyList(key):
    runningkey = []
    for c in key:
        if c.isalpha():
            runningkey.append(ord(c) - 97)

    return runningkey


def encrypt(message, key):
    runningkey = getRunningkeyList(key)
    keylength = len(runningkey)
    cipher = ""
    i = 0;
    for c in message:
        if c.isalpha():
            newchar = (ord(c) + runningkey[i % keylength] - 97) % 26
            cipher += chr(newchar + 97)
            i += 1
        else:
            cipher += c

    return cipher


def decrypt(cipher, key):
    runningkey = getRunningkeyList(key)
    keylength = len(runningkey)
    message = ""
    i = 0
    for c in cipher:
        if c.isalpha():
            newchar = (ord(c) - runningkey[i % keylength] - 97) % 26
            message += chr(newchar + 97)
            i += 1
        else:
            message += c

    return message


def writeToFile(file, text):
    file = open(file, 'w')
    file.write(text)