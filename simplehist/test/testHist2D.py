#!/usr/bin/env python
# encoding: utf-8
"""
testHist2D.py

Created by Nicholas Devenish on 2011-01-24.
"""

import unittest
from simplehist import Hist2D, BinError

class testHist2D(unittest.TestCase):
  def setUp(self):
    pass
  
  def testCreation(self):
    "Tests the basic creation"
    
    a = Hist2D([0,1,2],[0,1,2])
    
    self.assertEqual(a.rank,2)
    self.assertEqual(a.data.shape,(2,2))
    
    # self.assertEqual(a.bins, ((0,1,2),(0,1,2)))
    self.assertEqual(a.bins.x, (0,1,2))
    self.assertEqual(a.bins.y, (0,1,2))
  
  def testSetBin(self):
    "Tests setting bins"
    a = Hist2D([0,1],[0,1])
    a.bins = ((0,1,2,3),(0,1,2,3,4))
    
    def assignbin(value):
      a.bins = (value)
    self.assertRaises(BinError, assignbin, (0,1,2,3))

if __name__ == '__main__':
  unittest.main()