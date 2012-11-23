# coding: UTF-8
'''
Created on 20.11.2012

@author: Sho
'''
import unittest

import main


class Test(unittest.TestCase):


    def setUp(self):
        pass


    def tearDown(self):
        pass


    def getSizeTest(self):
        self.assertEqual(1, 1)
        self.assertEqual(1, 1)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()