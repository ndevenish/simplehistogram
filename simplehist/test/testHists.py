#!/usr/bin/env python
# encoding: utf-8
"""
testHists.py

Copyright (c) 2014 Nicholas Devenish <n.e.devenish@sussex.ac.uk>
"""

import numpy
from nose.tools import assert_raises
from simplehist import Hist

def testHistIndex():
  a = Hist(bins=[0,1,2,3], data=[0,1,2])
  assert a[0] == 0
  assert a[1] == 1
  assert a[2] == 2
  assert len(a) == 3

def testSlice():
  a = Hist(bins=[0,1,2,3], data=[0,1,2])
  assert len(a[1:]) == 2

def testPreserveDtype():
  "Tests that numpy array type is preserved"
  data = numpy.array([1, 2, 3], dtype=int)
  bins = [0, 1, 2, 3]
  a = Hist(bins, data=data)
  assert a.dtype == data.dtype
    
def testBasicFill():
  "Tests the elementary filling functions"
  a = Hist(range(101))
  a.fill(0.5)
  assert a[0] == 1.0
  # And, with weights
  a.fill(1.0, 0.5)
  assert a[1] == 0.5

def testArrayFill():
  a = Hist(range(101))
  a.fill([0.5, 1.5])
  assert a[0] == 1
  assert a[1] == 1
  a.fill([2.5, 3.5], [0.4, 0.5])
  assert a[2] == 0.4
  assert a[3] == 0.5
  

def testFillEdges():
  "Tests the filling edge cases"
  a = Hist(range(101))
  # Test that the overflow edge is good
  a.fill(100)
  assert a[99] == 0.0
  a.fill(99.9999999)
  assert a[99] == 1.0
  a.fill(0)
  assert a[0] == 1.0    

def testUfunc():
  """Test histograms going through a ufunc"""
  a = Hist(range(10))
  b = numpy.sum(a)
  assert b == 0
#   def testFlows1(self):
#     "Tests filling the underflow"
#     a = hists.Hist(range(101))
#     a.fill(-1)
#     self.assertEqual(a.underflow, 1.0)

#   def testFlows2(self):
#     "Test missing the overflow"
#     a = hists.Hist(range(101))
#     a.fill(99.9999999)
#     self.assertEqual(a.overflow, 0.0)

#   def testFlows3(self):
#     "Test filling the overflow"
#     a = hists.Hist(range(101))
#     a.fill(100)
#     self.assertEqual(a.overflow, 1.0)
  
def testNegativeAxis():
  "Tests creation and filling of negative bin sets"
  a = Hist(range(-10,11))
  a.fill(-9.5)
  assert a[0] == 1
  a.fill(-3.2)
  assert a[6] == 1

def testOutOfOrderBinning():
  assert_raises(ValueError, Hist, [0,1,3,2,4])
  a = Hist([0,1,2,3])
  # Setting after construction
  assert_raises(ValueError, lambda: setattr(a,"bins", [0,2,1,3]))
