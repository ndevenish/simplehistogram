#!/usr/bin/env python
# encoding: utf-8
"""
testHists.py

Created by Nicholas Devenish on 2011-01-12.
"""

import unittest
import hists
import numpy

class testHist(unittest.TestCase):
  def setUp(self):
    pass

  def testSimpleCreation(self):
    "Simple creation routines of a histogram"
    a = hists.Hist([0, 1, 2])
    # Test that this made sensible values
    self.assertEqual(a.data.size, 2)
    self.assertEqual(a.bins, [0, 1, 2])
  
  def testCreationWithData(self):
    "Test that data is allocated, and mismatched size data fails"
    a = hists.Hist([0, 1, 2], data=[1, 5])
    self.assertTrue((a.data == numpy.array([1,5])).all())
    self.assertRaises(hists.BinError, hists.Hist, [0, 1, 2], data=[1, 5, 2])
    
  def testNullCreation(self):
    "Null creation only works for zero bin entries"
    self.assertRaises(hists.BinError, hists.Hist, [0])
  
  def testChangeBins(self):
    """Tests correct behaviour when changing the number of bins"""
    a = hists.Hist([0, 1, 2])
    a.bins = [0, 1]
    self.assertEquals(a.data.size, 1)
  
  def test_bin_count(self):
    """Test the .bincount property makes sense"""
    bins = [0, 1]
    for x in range(2,10):
      bins.append(bins[-1]+1)
      a = hists.Hist(bins)
      self.assertEquals(a.bincount, x)
      self.assertEquals(a.bincount, a.data.size)
  
  def testInplaceArithmetic(self):
    "Tests the in-place arithmetic"
    bins = [0, 1, 2, 3]
    data = numpy.array([3, 1, 2])
    a = hists.Hist(bins, data)
    b = hists.Hist(bins, data)
    
    a += a
    self.assertTrue((a.data == data*2).all())
    a -= b
    self.assertTrue((a.data == data).all())
    a *= b
    self.assertTrue((a.data == data*data).all())
    a /= b
    self.assertTrue((a.data == data).all())
  
  def testArithmetic(self):
    "Tests the regular arithmetic"
    bins = [0, 1, 2, 3]
    data = numpy.array([3, 1, 2])
    a = hists.Hist(bins, data)
    b = hists.Hist(bins, data)
    
    c = a + a
    self.assertTrue((c.data == data*2).all())
    c = c - a
    self.assertTrue((c.data == data).all())
    c = a * a
    self.assertTrue((c.data == data*data).all())
    c = c / a
    self.assertTrue((c.data == data).all())
  
  def testNonClassIntegerArithmetic(self):
    "Tests arithmetic against non-Hist class values"
    bins = [0, 1]
    data = numpy.array([1])
    a = hists.Hist(bins, data)
    
    # Forward tests
    self.assertEqual((a + 5).data, 6)
    self.assertEqual((a - 5).data, -4)
    self.assertEqual((a * 10).data, 10)
    self.assertEqual((a / 2).data, 0.5)

    # Reverse tests
    self.assertEqual((5+a).data, 6)

  def testMismatchedData(self):
    "Checks that we cannot do operations on histograms with mismatched data"
    
    a = hists.Hist([0, 1, 2], data=numpy.zeros(2))
    b = hists.Hist([0, 1, 2], data=numpy.zeros((2,2)))
    
    self.assertRaises(TypeError, a.__add__, b)
    self.assertRaises(TypeError, a.__sub__, b)
    self.assertRaises(TypeError, a.__mul__, b)
    self.assertRaises(TypeError, a.__div__, b)
    
if __name__ == '__main__':
  unittest.main()