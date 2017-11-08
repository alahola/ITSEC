import argparse
import sys

from sectubs.vigenere.filecompresser import *
from sectubs.vigenere.vig_methods import *
from sectubs.vigenere.bruteforce import *
from sectubs.vigenere.crypto_analysis import *

#####
# Args-parser
#####

parser = argparse.ArgumentParser(
    "Attempts to break a vigenere-encrypted cipher of a given keylength"
)

parser.add_argument(
    "--keylen",
    "-k",
    metavar=("INT"),
    type=int,
    action="store",
    help="The keylength",
)

parser.add_argument(
    "--lang",
    "-l",
    action="store",
    default="eng",
    type=str,
    help="The language, either eng or ger (default: eng)",
)

parser.add_argument(
    "FILE",
    action="store",
    help="File to read from",
)
#####

#####
# Main part
#####
args = parser.parse_args()

lang = args.lang

keylen = args.keylen
if keylen <= 0:
    print("Keylength must be >= 0!")
    sys.exit()

cipher = compressFile(args.FILE)

best_score = -1
best_key = ""
best_message = ""

pos_keys = possible_keys(keylen)
pos_len = len(list(possible_keys(keylen)))

print("Possible Keys: " + str(pos_len))
pos = 1;
progress = 0;

for key in pos_keys:
    # Get score of every decrypted cipher
    encrypted = decrypt(cipher, key)
    score = analysis(encrypted, lang)
    if score > best_score:
        best_score = score
        best_key = key
        best_message = encrypted

    # Post progress
    newprogress = round((pos/pos_len)*100, 2)
    if newprogress > progress:
        progress = newprogress
        sys.stdout.write("\rProgress: " + str(progress) + "%")
        sys.stdout.flush()
    pos += 1

if best_score == -1:
    print("Could not be decrypted!")
else:
    print("\nBest score: " + str(best_score))
    print("Best key: " + str(best_key))
    print("Best message:")
    print(best_message)
#####
