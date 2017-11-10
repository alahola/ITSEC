def getPlain(e, n , c):
    steps = 1000000
    posM = []
    for i in range(1, steps):
        if c == i ** e % n:
            return i