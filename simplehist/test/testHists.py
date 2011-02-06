#!/usr/bin/env python
# encoding: utf-8
"""
testHists.py

Copyright (c) 2011 Nicholas Devenish <n.e.devenish@sussex.ac.uk>
"""

import unittest
import simplehist.hists as hists
import numpy
from copy import deepcopy


class testHist(unittest.TestCase):
  def testSimpleCreation(self):
    "Simple creation routines of a histogram"
    a = hists.Hist([0, 1, 2])
    # Test that this made sensible values
    self.assertEqual(a.data.size, 2)
    self.assertEqual(a.bins, (0, 1, 2))
  
  def testPreserveDtype(self):
    "Tests that numpy array type is preserved"
    data = numpy.array([1, 2, 3], dtype=int)
    bins = [0, 1, 2, 3]
    a = hists.Hist(bins, data=data)
    self.assertEqual(a.data.dtype, data.dtype)
    
  def testCreationWithData(self):
    "Test that data is allocated, and mismatched size data fails"
    a = hists.Hist([0, 1, 2], data=[1, 5])
    self.assertTrue((a.data == numpy.array([1,5])).all())
    self.assertRaises(hists.BinError, hists.Hist, [0, 1, 2], data=[1, 5, 2])
  
  def testFlows(self):
    "Tests that the under/overflows are created properly"  
    a = hists.Hist([0,1,2,3])
    self.assertEqual(a.underflow, 0.0)
    self.assertEqual(a.overflow, 0.0)
    a = hists.Hist([0,1,2,3], numpy.array([0,1,2]))
    self.assertEqual(a.underflow, 0)
    self.assertEqual(a.overflow, 0)
    
    # Change them, and verify that changing the data resets them
    a.underflow = 42
    a.overflow = 99
    a.data = numpy.array([0.,1.,2.])
    self.assertEqual(a.underflow, 0.0)
    self.assertEqual(a.overflow, 0.0)
  
  def testNullCreation(self):
    "Null creation only works for zero bin entries"
    self.assertRaises(hists.BinError, hists.Hist, [0])
  
  def testChangeBins(self):
    """Tests correct behaviour when changing the number of bins"""
    a = hists.Hist([0, 1, 2])
    a.bins = [0, 1]
    self.assertEquals(a.data.size, 1)
    # Check this was turned into a tuple
    def t():
      a.bins[1] = 4
    self.assertRaises(TypeError, t)
    # Check that bins must be in order
    def t():
      a.bins = [0, 2, 1, 3]
    self.assertRaises(hists.BinError, t)
      
    
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
    a //= hists.Hist(bins,data=[2,2,2])
    self.assertTrue((a.data == hists.Hist(bins,data=[1,0,1]).data).all())
    
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
    data = numpy.array([2])
    a = hists.Hist(bins, data)
    
    # Forward tests
    self.assertEqual((a + 5).data, 7)
    self.assertEqual((a - 5).data, -3)
    self.assertEqual((a * 10).data, 20)
    self.assertEqual((a / 2).data, 1)

    # Reverse tests
    self.assertEqual((5+a).data, 7)

  def testNonClassFloorDivArithmetic(self):
    """Tests the floor division, using float arrays"""
    bins = [0, 1]
    data = numpy.array([2.])
    a = hists.Hist(bins, data)
    a //= 2
    self.assertAlmostEqual(a.data, 1)
    a[0] = 2.
    a //= 3
    self.assertAlmostEqual(a.data, 0)
    
  def testMismatchedData(self):
    "Checks that we cannot do operations on histograms with mismatched data"
    
    a = hists.Hist([0, 1, 2], data=numpy.zeros(2))
    b = hists.Hist([0, 1, 2], data=numpy.zeros((2,2)))
    
    self.assertRaises(TypeError, a.__add__, b)
    self.assertRaises(TypeError, a.__sub__, b)
    self.assertRaises(TypeError, a.__mul__, b)
    self.assertRaises(TypeError, a.__div__, b)
  
  def testEmptyList(self):
    "Tests the creation of histograms from an empty list"
    a = hists.Hist([])
    
  def testRank(self):
    "Tests the histogram rank property"
    a = hists.Hist([])
    self.assertEqual(a.rank, 1)
    def t():
      a.rank = 2
    self.assertRaises(AttributeError, t)
  
  def testGetItem(self):
    "Tests accessing the data through the histogram[]"
    a = hists.Hist([0,1,2,3,4], data=(0,0,1,0))
    self.assertEqual(a[2], 1)
  
  def testSetItem(self):
    "Tests setting bin values through []"
    a = hists.Hist([0,1,2,3,4], data=(0,0,0,0))
    a[2] = 1
    self.assertEqual(a[2], 1)
    
  def testRepr(self):
    "Test grabbing of the __repr__ string"
    a = hists.Hist([-1,0,1,2], data=(0,0,0))
    r = repr(a)
  
  def testIntegrate(self):
    "Tests integrating of the histogram"
    a = hists.Hist([-1,0,1,2], data=(0,1.3345,0))
    self.assertAlmostEqual(a.integral(), 1.3345)
    
    # And overflow
    a.fill(-10)
    self.assertAlmostEqual(a.integral(), 1.3345)
    self.assertAlmostEqual(a.integral(all=True), 2.3345)
    
class testHistFilling(unittest.TestCase):
  def setUp(self):
    pass
    
  def testBasicFill(self):
    "Tests the elementary filling functions"
    a = hists.Hist(range(101))
    a.fill(0.5)
    self.assertEqual(a.data[0], 1.0)
    # And, with weights
    a.fill(1.0, 0.5)
    self.assertEqual(a.data[1], 0.5)
  
  def testFillEdges(self):
    "Tests the filling edge cases"
    a = hists.Hist(range(101))
    # Test that the overflow edge is good
    a.fill(100)
    self.assertEqual(a.data[99], 0.0)
    a.fill(99.9999999)
    self.assertEqual(a.data[99], 1.0)
    a.fill(0)
    self.assertEqual(a.data[0], 1.0)
    
    
  def testFlows1(self):
    "Tests filling the underflow"
    a = hists.Hist(range(101))
    a.fill(-1)
    self.assertEqual(a.underflow, 1.0)

  def testFlows2(self):
    "Test missing the overflow"
    a = hists.Hist(range(101))
    a.fill(99.9999999)
    self.assertEqual(a.overflow, 0.0)

  def testFlows3(self):
    "Test filling the overflow"
    a = hists.Hist(range(101))
    a.fill(100)
    self.assertEqual(a.overflow, 1.0)
  
  def testNegativeAxis(self):
    "Tests creation and filling of negative bin sets"
    a = hists.Hist(range(-10,11))
    a.fill(-9.5)
    self.assertEqual(a.data[0], 1)
    a.fill(-3.2)
    self.assertEqual(a.data[6], 1)
  
  def testMergebins(self):
    "Tests Mergebinning a histogram"
    a = hists.Hist([0,1,2,3,4,5,6])
    self.assertEqual(a.bincount, 6)
    a.fill(1.5)
    a.fill(2.5)
    a.fill(3.5)

    b = deepcopy(a)
    b.mergebins(2)
    self.assertEqual(b.bincount, 3)
    expected = [1,2,0]
    for bin in range(3):
      self.assertAlmostEqual(b.data[bin], expected[bin])
    
    # Test odd-aspect merging
    c = deepcopy(a)
    c.mergebins(4)
    self.assertEqual(c.bincount, 2)
    expected = [3,0]
    for bin in range(2):
      self.assertAlmostEqual(c.data[bin], expected[bin])
  
  def testAreaMergebins(self):
    """Tests mergebinning by bin area counts"""
    a = hists.Hist([0,1,2,4,5,8,12], data=[0,1,1,2,3,1.2])
    # Width = 1,1, 2,1, 3,4
    # Data  = 0,1, 1,2, 3,1.2
    a.mergebins(2, area=True)
    self.assertEqual(a.bincount, 3)
    expected = [0.5,4./3,(9+4*1.2)/7]
    for bin in range(a.bincount):
      self.assertAlmostEqual(a.data[bin], expected[bin])
  
  def testComplexMergeBin(self):
    """Tests the failure mode of a complex hist from data"""
    data = hists.Hist((0.0, 0.5, 0.75, 1.0, 1.25, 1.5, 1.75, 2.0, 2.25, 2.5, 2.75, 3.0, 3.25, 3.5, 3.75, 4.0, 4.25, 4.5, 4.75, 5.0, 5.25, 5.5, 5.75, 6.0, 6.25, 6.5, 6.75, 7.0, 7.25, 7.5, 7.75, 8.0, 8.25, 8.5, 8.75, 9.0, 9.25, 9.5, 9.75, 10.0, 10.25, 10.5, 10.75, 11.0, 11.25, 11.5, 11.75, 12.0, 12.25, 12.5, 12.75, 13.0, 13.25, 13.5, 13.75, 14.0, 14.25, 14.5, 14.75, 15.0, 15.25, 15.5, 15.75, 16.0, 16.25, 16.5, 16.75, 17.0, 17.25, 17.5, 17.75, 18.0, 18.25, 18.5, 18.75, 19.0, 19.25, 19.5, 19.75, 20.0, 21.0, 22.0, 23.0, 24.0, 25.0, 26.0, 27.0, 28.0, 29.0, 30.0, 32.0, 34.0, 36.0, 38.0, 40.0, 42.0, 44.0, 46.0, 48.0, 50.0, 200.0),data=numpy.array([ 0.        ,  0.39236547,  0.41352704,  0.37823504,  0.22213782,
            0.1096127 ,  0.07590537,  0.05410349,  0.05589178,  0.01672955,
            0.02912907,  0.        ,  0.01633081,  0.        ,  0.01905453,
            0.        ,  0.0136084 ,  0.0089573 ,  0.00382536,  0.01213058,
            0.00508681,  0.01962308,  0.00892336,  0.01173807,  0.        ,
            0.00382451,  0.        ,  0.00921557,  0.00391108,  0.        ,
            0.00674696,  0.00422079,  0.00578021,  0.00790876,  0.0040755 ,
            0.        ,  0.        ,  0.        ,  0.        ,  0.00396123,
            0.00845284,  0.        ,  0.        ,  0.        ,  0.00595007,
            0.00704693,  0.        ,  0.        ,  0.        ,  0.        ,
            0.        ,  0.        ,  0.        ,  0.        ,  0.00673726,
            0.00562558,  0.        ,  0.00878138,  0.        ,  0.        ,
            0.00751557,  0.        ,  0.00757781,  0.00790601,  0.        ,
            0.        ,  0.00437298,  0.        ,  0.        ,  0.01535721,
            0.        ,  0.        ,  0.01340345,  0.        ,  0.        ,
            0.        ,  0.        ,  0.        ,  0.        ,  0.        ,
            0.00438391,  0.        ,  0.        ,  0.        ,  0.        ,
            0.        ,  0.00547386,  0.01746112,  0.        ,  0.        ,
            0.01730692,  0.        ,  0.        ,  0.01814207,  0.        ,
            0.02847297,  0.        ,  0.        ,  0.        ,  0.01451508]))
    data.mergebins(3,area=True)
  
if __name__ == '__main__':
  unittest.main()