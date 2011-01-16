SimpleHist
==========

:Description: A very simple ndarray-based histogram class.
:Author:      Nicholas Devenish

Overview
--------

Matplotlib histograms are geared around drawing, not
data manuipulation. Numpy direct support for histograms is
extremely limited, and not very different from matpotlib.
This is intended to turn into a set of very lightweight classes
for shuffling data around. This is very much a work-in-progress.

The only required depenency is numpy, and the package is designed
to work for python > 2.6

Type "make test" to run the core unit tests. Some tests, such
as the pyROOT-based tests, must be run explicitly (or through
python2.7> unittest discovery). At the moment, the ROOT test
requires pyROOT, which is why it doesn't run by default as not
many people have (or need) this dependency. 

Usage
-----

A summary of usage, taken from the hists.py docstring follows:

Importing:
  >>> from simplehist import Hist

Initialise with bin indices:
  >>> a = Hist([0, 1, 2, 3])
  >>> a.bincount
  3
  >>> a.bins
  (0, 1, 2, 3)
  >>> a.data
  array([ 0.,  0.,  0.])

Optionally include data:
  >>> a = Hist([0, 1, 2, 3], data=[1, 0.2, 3])
  >>> a.data
  array([ 1. ,  0.2,  3. ])

Or just specify the blank data type:
  >>> a = Hist([0, 1, 2, 3], dtype=int)
  >>> a.data
  array([0, 0, 0])

You can do arithmetic operations in place or seperately:
  >>> a = Hist([0, 1, 2, 3], data=[1, 0.2, 3])
  >>> b = a + a
  >>> b -= a
  >>> a.data == b.data
  array([ True,  True,  True], dtype=bool)  

And you can fill bins from values:
  >>> a = Hist([0,1,2,3])
  >>> a.fill(1.4, weight=3)
  >>> a.data
  array([ 0.,  3.,  0.])

Even out of range:
  >>> a = Hist([0,1])
  >>> a.fill(-10)
  >>> a.underflow
  1.0

If you use pyROOT, you can convert from 1D histograms:
  >>> type(source)
  <class 'ROOT.TH1D'>
  >>> convert = fromTH1(source)
  >>> type(convert)
  <class 'simplehist.hists.Hist'>

And you can draw histograms, using any of the options
that can be passed to matplotlib.pyplot.hist:

  >>> hist_object.draw_hist(lw=2)
