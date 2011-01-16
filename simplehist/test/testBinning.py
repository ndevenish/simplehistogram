#!/usr/bin/env python
# encoding: utf-8
"""
testBinning.py

Tests the simplehist.binning module

Copyright (c) 2011 Nicholas Devenish
"""

import unittest

import numpy
import simplehist.binning as binning

class testBinningScheme(unittest.TestCase):
  def setUp(self):
    pass

  def testCreation(self):
    "Tests creation of BinningScheme objects"
    a = binning.BinningScheme([0,1])
    self.assertEqual(a[0], 0)
    self.assertEqual(a[1], 1)
  
  def testNumpyCreation(self):
    "Tests creation from a numpy object"
    bins = numpy.array([-5,1])
    a = binning.BinningScheme(bins)
    self.assertEqual(len(a), 1)
    bins = numpy.array([0,1,2])
    a = binning.BinningScheme(bins)
    self.assertEqual(len(a), 2)
    bins = numpy.array([0.,1.,2.])
    a = binning.BinningScheme(bins)
    self.assertEqual(len(a), 2)
  
  def testLen(self):
    "Tests retrieving the length of the binningscheme"
    # Start with empty schemes
    a = binning.BinningScheme([])
    self.assertEqual(len(a), 0)    
    # And single bin schemes
    a = binning.BinningScheme([0,1])
    self.assertEqual(len(a), 1)
  
  def testCreateSmall(self):
    "Tests creation with invalid sources"
    self.assertRaises(binning.BinError, binning.BinningScheme, [0])
    self.assertRaises(TypeError, binning.BinningScheme)
  
  def testEmpty(self):
    "Tests creation of empty bins"
    a = binning.BinningScheme([])
    self.assertEqual(len(a), 0)
  
  def testGetEdges(self):
    "Tests retrieving of the edge array"
    bins = [-1,1,2]
    a = binning.BinningScheme(bins)
    self.assertEqual(tuple(bins), a.edges)
    # Test a larger set
    for i in range(1000):
      bins.append(sum(bins[-2:]))
      a = binning.BinningScheme(bins)
      self.assertEqual(tuple(bins), a.edges)
    
  def testGetLowEdges(self):
    "Tests the getting of the low-edge array"
    bins = [-1,1,2]
    a = binning.BinningScheme(bins)
    self.assertEqual(tuple(bins)[:-1], a.lowedges)
    # Test a larger set
    for i in range(1000):
      bins.append(sum(bins[-2:]))
      a = binning.BinningScheme(bins)
      self.assertEqual(tuple(bins)[:-1], a.lowedges)
  
  def testGetCenters(self):
    "Tests getting the bin centers"
    # Build the initial test array
    bins = numpy.array([-1.,1.,2.])
    centers = bins[:-1] + (bins[1:]-bins[:-1])/2.
    a = binning.BinningScheme(bins)
    self.assertEqual(tuple(centers), a.centers)
    # Test a larger set
    for i in range(100):
      bins = numpy.hstack([bins, sum(bins[-2:])])
      centers = bins[:-1] + (bins[1:]-bins[:-1])/2.
      a = binning.BinningScheme(bins)
      self.assertEqual(tuple(centers), a.centers)
    
if __name__ == '__main__':
  unittest.main()