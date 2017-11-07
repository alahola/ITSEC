def read(filename: str):
    alphabeticCharacters = "abcdefghijklmnopqrstuvwxyz"
    file = open(filename)
    rawdata = file.read()
    file.close()
    data = ""
    for c in rawdata:
        if alphabeticCharacters.find(c.lower()) >= 0:
            data += c.lower()
    return data



def write(writin: str, filename: str):
    file = open(filename, "w")
    file.write(writin)
    file.close()


def lineGenerator(filename: str):
    file = open(filename, "r")
    line = file.readline()
    while line != "":
        ret = ""
        for c in line:
            if c != "'":
                ret += c
        yield ret
        line = file.readline()
    file.close()


def readWordlistMain(filename: str):
    file = open(filename)
    line = "this will be skipped"
    index = 1
    chars = {}
    while line != "":
        line = file.readline()
        if index < 27:
            chars[line[0]] = float(line[4:len(line) - 2])
        elif index < 27 + 20:
            chars[line[:2]] = float(line[5:len(line) - 2])
        elif index < 27 + 2 * 20:
            chars[line[:3]] = float(line[6:len(line) - 2])
        elif index < 27 + 3 * 20:
            chars[line[:4]] = float(line[7:len(line) - 2])
        index += 1
    file.close()
    return chars


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