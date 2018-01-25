#!/usr/bin/env python3

'''
@author: Christian Wressnegger
'''

import os
import subprocess
import unittest

unittest.TestLoader.sortTestMethodsUsing = None


class Ex08(unittest.TestCase):

    SCORE = 0

    def xss_read_url(self, var):
        my_dir = os.path.dirname(os.path.abspath(__file__))
        try:
            url = None
            with open(os.path.join(my_dir, "xss-var{}.url".format(var)), 'r') as f:
                for line in f:
                    url = line
                    break
            self.assertTrue(
                url and url.startswith("http://weird.sec.tu-bs.de"), "No URL!?")
        except IOError:
            self.assertTrue(False, "Unable to read file")

    def webapp_read_urls(self, var):
        my_dir = os.path.dirname(os.path.abspath(__file__))
        try:
            url = None
            with open(os.path.join(my_dir, "webapp-task{}.url".format(var)), 'r') as f:
                for line in f:
                    url = line

                    self.assertTrue(
                        url and url.startswith("http://"), "No URL!?")

            self.assertTrue(url, "No URLs included :/")

        except IOError:
            self.assertTrue(False, "Unable to read file")

    def test_01_xss_var0(self):
        self.xss_read_url(0)
        Ex08.SCORE += 2

    def test_01_xss_var1(self):
        self.xss_read_url(1)
        Ex08.SCORE += 2

    def test_01_xss_var2(self):
        self.xss_read_url(2)
        Ex08.SCORE += 2

    def test_01_xss_var3(self):
        self.xss_read_url(3)
        Ex08.SCORE += 2

    def test_01_xss_var4(self):
        self.xss_read_url(4)
        Ex08.SCORE += 2

    def test_01_xss_var5(self):
        self.xss_read_url(5)
        Ex08.SCORE += 2

    def test_02_task_b(self):
        self.webapp_read_urls('b')
        Ex08.SCORE += 1

    def test_02_task_c(self):
        self.webapp_read_urls('c')
        Ex08.SCORE += 2

    def test_02_task_d(self):
        self.webapp_read_urls('d')
        Ex08.SCORE += 2

    def test_02_task_e(self):
        self.webapp_read_urls('e')
        Ex08.SCORE += 2

    def test_02_task_f(self):
        self.webapp_read_urls('f')
        Ex08.SCORE += 3

    def test_XX(self):
        print("[*] Total score for Exercise 08: {}/26".format(Ex08.SCORE))


if __name__ == "__main__":
    unittest.main()
