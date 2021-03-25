import copy
import os.path as path
import shutil
import unittest

import sltxpkg.config as sc
import sltxpkg.globals as sg

import sltxtest.util.dir as sud
import sltxtest.util.globals as sug


class TestCache(unittest.TestCase):

    def test_local_pull(self):
        print("123")

    def tearDown(self):
        sug.restore_configuration()


if __name__ == '__main__':
    unittest.main()
