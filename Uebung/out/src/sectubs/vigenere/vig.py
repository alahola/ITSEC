import argparse

from sectubs.vigenere.filecompresser import compressFile
from sectubs.vigenere.vig_methods import encrypt, decrypt, writeToFile


#####
# Args-parser
#####

parser = argparse.ArgumentParser(
    "Encrypts or decrypts a file using Vigenere cipher"
)

actions = parser.add_mutually_exclusive_group(required=True)
actions.add_argument(
    "--encrypt",
    "-e",
    nargs=1,
    metavar=("KEY"),
    action="store",
    help="Encrypt using key",
)

actions.add_argument(
    "--decrypt",
    "-d",
    nargs=1,
    metavar=("KEY"),
    action="store",
    help="Decrypt using key",
)

parser.add_argument(
    "--outfile",
    "-o",
    metavar=("FILE"),
    action="store",
    help="File to output result to",
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

if args.encrypt is not None:

    key = str(args.encrypt).lower()
    message = compressFile(args.FILE)
    out = encrypt(message, key)

else:

    key = str(args.decrypt).lower()
    cipher = compressFile(args.FILE)
    out = decrypt(cipher, key)

if args.outfile is not None:
    writeToFile(args.outfile, out)
    print("Printed to file: " + args.outfile)
else:
    print(out)
#####
