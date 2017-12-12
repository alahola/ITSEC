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
    import ex05_testdata as testdata  # @UnresolvedImport @UnusedImport

except:
    import ex05_testdata as testdata  # @UnresolvedImport


import os
import subprocess
import unittest


unittest.TestLoader.sortTestMethodsUsing = None


class Ex05(unittest.TestCase):

    SCORE = 0

    @staticmethod
    def call(tool, params):
        my_dir = os.path.dirname(os.path.abspath(__file__))
        script = os.path.join(my_dir, tool)
        cmd = 'python3 "{}" {}'.format(script, params)

        p = subprocess.Popen(
            cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        out, err = p.communicate()

        return out, err, p.returncode

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

#     def test_03_sendpacket(self):
#         _, out, _ = Ex05.call("send_packet.py", "")
#         self.assertTrue(testdata.verify_synopsis("send_packet", out))
#         Ex05.SCORE += 8

    def test_04_portknocker(self):
        _, out, _ = Ex05.call(os.path.join("port_knocker", "client.py"), "")
        self.assertTrue(testdata.verify_synopsis("client", out))
        Ex05.SCORE += 6

        _, out, _ = Ex05.call(os.path.join("port_knocker", "server.py"), "")
        self.assertTrue(testdata.verify_synopsis("server", out))
        Ex05.SCORE += 6

    def test_XX(self):
        print("[*] Total score for Exercise 7: {}/20".format(Ex05.SCORE))


if __name__ == "__main__":
    unittest.main()
