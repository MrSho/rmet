# coding: UTF-8
'''
Created on 20.11.2012

@author: Sho
'''
import unittest
import StringIO

import misc


class get_fnumTest(unittest.TestCase):


    def setUp(self):
        inputStr = '\x01\x7f\x81\x00\x81\x7f\x82\x01\x9C\xCD\x54'
        self.outputTplb = (0x1, 0x7f, 0x80, 0xff, 0x101, 0x726d4)
                
        self.TestBuff = StringIO.StringIO(inputStr)


    def tearDown(self):
        self.TestBuff.close()


    def test_getSize(self):
        for i in xrange(6):
            b = misc.get_fnum(self.TestBuff)
            self.assertEqual(b, self.outputTplb[i])

class get_fnum_countTest(unittest.TestCase):


    def setUp(self):
        inputStr = '\x01\x7f\x81\x00\x81\x7f\x82\x01\x9C\xCD\x54'
        self.outputTplb = (0x1, 0x7f, 0x80, 0xff, 0x101, 0x726d4)
        self.outputTpls = ('\x01','\x7f', '\x81\x00','\x81\x7f', '\x82\x01', '\x9C\xCD\x54')
                
        self.TestBuff = StringIO.StringIO(inputStr)


    def tearDown(self):
        self.TestBuff.close()


    def test_getSize(self):
        for i in xrange(6):
            b, s = misc.get_fnum_count(self.TestBuff)
            self.assertEqual(b, self.outputTplb[i])
            self.assertEqual(s, self.outputTpls[i])
            

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()