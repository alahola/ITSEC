#!/usr/bin/env python3

'''
@author: Christian Wressnegger
'''

try:
    # For evaluating the exercises we'll provide a similar but
    # different configuration that contains alternative input
    # values than those provided in the script that was handed
    # out. Develop your solution robust enough to work with
    # various kinds and variations of input.
    import ex03_testdata_lecturer as testdata

except:
    import ex03_testdata as testdata


import os
import re
import subprocess
import unittest

import urllib.request as request


unittest.TestLoader.sortTestMethodsUsing = None


class Ex03(unittest.TestCase):

    SCORE = 0

    @staticmethod
    def call(tool, params):
        my_dir = os.path.dirname(os.path.abspath(__file__))
        script = os.path.join(my_dir, tool)
        cmd = 'python "{}" {}'.format(script, params)

        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
        out, _ = p.communicate()

        return out, p.returncode

    def read_line(self, fname):
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

    def test_03_mitm(self):
        out, _ = Ex03.call("mitm.py", 'weird.sec.tu-bs.de 3333')
        self.assertTrue(testdata.verify_msgs(out))

        s = self.read_line("flag.txt")
        self.assertTrue(testdata.verify_flag(s))
        Ex03.SCORE += 12

    def test_04_gpg(self):
        fprint = self.read_line("fingerprint.txt").split('\t')[-1]
        fprint = re.sub(r'\s+', '', fprint.strip()).upper()
        self.assertEqual(len(fprint), 40)
        Ex03.SCORE += 1

        URL = "http://pgp.mit.edu/pks/lookup?search=0x{}".format(fprint)
        page = request.urlopen(URL)
        s = page.read()

        names = self.read_line(os.path.join(".", "NAME")).split(' ')[:2]
        for x in names:
            self.assertIn(
                str.encode(x.lower()), s.lower(), "Cannot find your key and name online :(")

        Ex03.SCORE += 2

    def test_XX(self):
        print("[*] Total score for Exercise 5: {}/15".format(Ex03.SCORE))


if __name__ == "__main__":
    unittest.main()
