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

    # Test various valid combinations
    a.bins = ((0,1),(0,1))
    a.bins = ((0,1),[0,1])
    
    def assignbin(value):
      a.bins = (value)
    self.assertRaises(BinError, assignbin, (0,1,2,3))
    self.assertRaises(BinError, assignbin, ((0,),(0,1)))
    self.assertRaises(BinError, assignbin, ((0,1),(0,)))
    self.assertRaises(BinError, assignbin, ((0,),(0,1)))
    self.assertRaises(BinError, assignbin, ([],(0,1)))
    self.assertRaises(BinError, assignbin, ((0,1),[]))

  def testBinSetData(self):
    """Test that settng bins changes the data array"""
    a = Hist2D([0,1],[0,1])
    self.assertEqual(a.data.shape, (1,1))
    a.bins = [[0,1,2],[0,1,2,3,4]]
    self.assertEqual(a.data.shape, (2,4))
  
  def testBinCount(self):
    """Tests the .bincount property"""
    a = Hist2D([0,1],[0,1])
    self.assertEqual(a.bincount, (1,1))
    a = Hist2D([0,1,2,3],[0,1])
    self.assertEqual(a.bincount, (3,1))
    
  def testSetData(self):
    """Tests assigning data"""
    a = Hist2D([0,1],[0,1])
    a.data = [[0]]

    # Test invalid assignments
    def assigndata(value):
      a.data = value
    self.assertRaises(BinError, assigndata, [0])
    self.assertRaises(BinError, assigndata, [[0],[0]])
  
if __name__ == '__main__':
  unittest.main()