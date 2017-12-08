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
    import ex04_testdata_lecturer as testdata

except:
    import ex04_testdata as testdata


import os
import subprocess
import unittest

import urllib.request as request


unittest.TestLoader.sortTestMethodsUsing = None


class Ex04(unittest.TestCase):

    SCORE = 0

    @staticmethod
    def call(tool, params):
        my_dir = os.path.dirname(os.path.abspath(__file__))
        script = os.path.join(my_dir, tool)
        cmd = 'python3 "{}" {}'.format(script, params)

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

    def test_05_weirdclient(self):
        out, _ = Ex04.call("weird_client.py", "weird.sec.tu-bs.de 6666")
        self.assertTrue(testdata.verify_msgs(out))

        s = self.read_line("flag.txt")
        self.assertTrue(testdata.verify_flag(s))
        Ex04.SCORE += 10

    def test_XX(self):
        print("[*] Total score for Exercise 6: {}/10".format(Ex04.SCORE))


if __name__ == "__main__":
    unittest.main()
