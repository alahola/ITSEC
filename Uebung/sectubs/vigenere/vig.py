
def encrypt(plain: str, key: str):
    ret = ""
    keycursor = 0
    for c in plain:
        if keycursor == len(key):
            keycursor = 0
        ch = ord(c) + ord(key[keycursor]) - 97
        if ch > 122:
            ret += chr(ch-26)
        else:
            ret += chr(ch)
        keycursor += 1
    return ret


def decrypt(cipher: str, key: str):
    ret = ""
    keycursor = 0
    for c in cipher:
        if keycursor == len(key):
            keycursor = 0
        ch = ord(c) - ord(key[keycursor]) + 97
        if ch < 97:
            ret += chr(ch+26)
        else:
            ret += chr(ch)
        keycursor += 1
    return ret