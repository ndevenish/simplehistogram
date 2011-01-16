#!/usr/bin/env python
# encoding: utf-8
"""
testROOT.py

Tests the creation of a Hist object from a ROOT histogram. This is
in a separate tests because I wanted to remove the expicit dependence
on pyROOT (and didn't want to put the effort into duplicating the
subtleties of the ROOT histogram interfaces)

Copyright (c) 2011 Nicholas Devenish <n.e.devenish@sussex.ac.uk>
"""

import unittest
from ROOT import TH1D
import simplehist.hists as hists

class TestROOT(unittest.TestCase):
  def setUp(self):
    # Build a test TH1
    pass
  
  def testBinCount(self):
    "Tests basic copying of bin counts"
    Rh = TH1D("test","test",10,0,10)
    h = hists.fromTH1(Rh)
    # Test the bin count is good
    self.assertEqual(h.bincount, 10)

  def testBinCount(self):
    "Tests copying over the bin boundaries"
    Rh = TH1D("test","test",10,-5,55.332)
    h = hists.fromTH1(Rh)
    # Test the bin indices
    for bin in range(1,12):
      message="Error testing bin {0}".format(bin)
      self.assertAlmostEqual(h.bins[bin-1], Rh.GetBinLowEdge(bin),msg=message)
  
  def testBinContentCount(self):
    "Tests that bin contents are copied"
    Rh = TH1D("test","test",10,0,10)
    Rh.FillRandom("pol0")
    h = hists.fromTH1(Rh)
    # Test the bin indices
    for bin in range(1,11):
      message="Error testing bin {0}".format(bin)
      self.assertAlmostEqual(h[bin-1], Rh.GetBinContent(bin),msg=message)
  
  def testOverflow(self):
    "Test the overflow is copied"
    Rh = TH1D("test","test",1,0,1)
    Rh.Fill(10)
    h = hists.fromTH1(Rh)
    self.assertAlmostEqual(h.overflow, 1)
    
  def testUnderflow(self):
    "Test that the underflow is copied"
    Rh = TH1D("test","test",1,0,1)
    Rh.Fill(-10)
    h = hists.fromTH1(Rh)
    self.assertAlmostEqual(h.underflow, 1)
    
    
if __name__ == '__main__':
  unittest.main()