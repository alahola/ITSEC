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
    import ex02_testdata_lecturer as testdata

except:
    import ex02_testdata as testdata


import os
import subprocess
import unittest

unittest.TestLoader.sortTestMethodsUsing = None


class Ex02(unittest.TestCase):

    SCORE = 0

    @staticmethod
    def call(tool, params):
        my_dir = os.path.dirname(os.path.abspath(__file__))
        script = os.path.join(my_dir, tool)
        cmd = 'python3 "{}" {}'.format(script, params)

        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
        out, _ = p.communicate()

        return out, p.returncode

    def test_02_rsa(self):
        for d in testdata.RSA:
            msg, _ = Ex02.call(os.path.join(
                "rsa", "crack_rsa.py"), "-e {e} -n {n} --ciphertext {ciphertext}".format(**d))

            msg = msg.strip().decode('ascii')
            self.assertEqual(msg, str(d['msg']))
        Ex02.SCORE += 7

    def test_04_dh(self):
        for d in testdata.DH:
            key, _ = Ex02.call(os.path.join(
                "dh", "crack_dh.py"), "-g {g} -n {n} --alice {alice} --bob {bob}".format(**d))

            key = key.strip().decode('ascii')
            self.assertEqual(key, str(d['key']))
        Ex02.SCORE += 7

    def test_XX(self):
        print("[*] Total score for Exercise 02: {}/14".format(Ex02.SCORE))


if __name__ == "__main__":
    unittest.main()
