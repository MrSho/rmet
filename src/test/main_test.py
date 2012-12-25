'''
Created on 01.12.2012

@author: Sho
'''
import unittest
import main


class ReadFilesTest(unittest.TestCase):


    def setUp(self):
        pass


    def tearDown(self):
        pass


    def testMain(self):
        DB = main.read_db()
        md = dict()
        for m in main.get_maps_list():
            md[m] = main.read_map(m)
        self.assertEqual(repr(md['Map0020.lmu'].SaveCount), '1654')
        self.assertEqual(repr(md['Map0389.lmu'].SaveCount), '1640')
        self.assertEqual(repr(md['Map0023.lmu'].SaveCount), '1558')
        self.assertEqual(repr(md['Map0273.lmu'].SaveCount), '449')
        self.assertEqual(repr(md['Map0399.lmu'].SaveCount), '319')

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()