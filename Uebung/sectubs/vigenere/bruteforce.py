#####
# Methods
#####
import itertools

"""
    Creates all possible keys with a given length from a given charset
    :param length: The length of the key
    :param charset: The charset the key is made out of (default: small-letter alphabet)
    :return: A generator containing all possible combinations
"""
def possible_keys(length: int, charset ='abcdefghijklmnopqrstuvwxyz'):
    return (''.join(candidate)
        for candidate in itertools.chain.from_iterable(itertools.product(charset, repeat=i)
        for i in range(length, length + 1)))

#####