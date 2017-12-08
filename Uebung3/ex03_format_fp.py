#!/usr/bin/env python

'''
@author: Christian Wressnegger
'''

import argparse
import os
import re
import sys

try:
    from urllib.request import urlopen
except ImportError:
    from urllib import urlopen


def __read_line(self, fname):
    my_dir = os.path.dirname(os.path.abspath(__file__))
    try:
        line = None
        with open(os.path.join(my_dir, fname), 'r') as f:
            for line in f:
                break

        self.assertTrue(line, "No data provided")
    except IOError:
        self.assertTrue(False, "Unable to read file")

    return line


def error(s):
    sys.stderr.write("[!] {}\n".format(s))


def main(args):
    fprint = re.sub(r'\s+', '', args.fingerprint.strip()).upper()
    if len(fprint) != 40:
        error("The length of the fingerprint seems to be off :(")
        return 1

    URL = "http://pgp.mit.edu/pks/lookup?search=0x{}".format(fprint)
    page = urlopen(URL)
    s = page.read()

    if str.encode(args.name) not in s:
        error("Cannot find your key and name online :(")
        return 2

    fprint = ' '.join(str(fprint[i:i + 4]) for i in range(0, len(fprint), 4))
    print("{}\t{}".format(args.name, fprint))
    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--name", metavar="STR", action="store", type=str, default=None, required=True,
                        help="Your GPG fingerprint.")
    parser.add_argument("--fingerprint", metavar="STR", action="store", type=str, default=None,  required=True,
                        help="Your GPG fingerprint.")

    args = parser.parse_args()

    try:
        sys.exit(main(args))
    except Exception as e:
        sys.stderr.write("{}\n".format(e))
        sys.exit(666)
