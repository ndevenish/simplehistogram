# coding: utf-8

"""
hists.py

Copyright (c) 2011 Nicholas Devenish <n.e.devenish@sussex.ac.uk>

An easy, quick, lightweight histogram class based on ndarray

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
"""

import numpy
import copy

from binning import BinError
import binning

def _match_rank(f):
  """Decorator to ensure that the second argument matches rank"""
  def checkrank(self, other):
    if isinstance(other, Hist):
      if self.data.size != other.data.size:
        raise TypeError("Histogram data arrays do not match size! {0} != {1}"
                        .format(self.data.size, other.data.size))
    return f(self, other)
  return checkrank

class Hist(object):
  """ndarray based histogram object"""
  def __init__(self, bins, data=None, dtype=float):
    """Initialise a new Hist.
    
    bins:  The binning scheme for this histogram
    data:  The data to fill these bins. Must be the same size as bins (Optional)
    dtype: The numpy data type to create the data array with, if data is not provided
    """
    super(Hist, self).__init__()
    
    # Assign the internal variable so that bin assignment can test conditions
    # self._bins = bins
    self._bins = None
    self.bins = bins
    
    # Assign the data, if we have been given any
    if data is None:
      self.data = numpy.zeros(self.bincount, dtype=dtype)
    else:
      self.data = numpy.array(data)

  @property
  def rank(self):
    return 1
  
  @property
  def bins(self):
    "Contains the bin values"
    return self._bins
    
  @bins.setter
  def bins(self, newbins):
    """Sets the bin array"""
    # Is the bin array a valid size? (i.e. > 1 or zero)
    if len(newbins) == 1:
      raise BinError("Must provide more that one value for a single bin")
      
    # Calculate the number of bins
    if len(newbins) == 0:
      bincount = 0
    else:
      bincount = len(newbins)-1
    
    # Ensure the bins are numerically sequential
    if not tuple(newbins) == tuple(sorted(newbins)):
      raise BinError("Bins must be numerically ascending")
    
    # Do we need to resize our data?
    if self._bins and len(newbins) != len(self._bins):
      self.data.resize(bincount)
    
    self._bins = tuple(newbins)
  
  @property
  def bincount(self):
    "Returns the number of bins"
    return max(len(self._bins)-1, 0)
  
  @property
  def data(self):
    "Returns the data object"
    return self._data
  
  @data.setter
  def data(self, newdata):
    "Sets the internal data object"
    # Check this matches our bin count
    if len(newdata) == self.bincount:
      self._data = numpy.array(newdata)
    else:
      raise BinError("Data incorrect dimensions! Data size {0} != {1} bins".format(len(newdata), len(self._bins)-1))
    # Build the under and overflows
    self.underflow = self._data.dtype.type(0.0)
    self.overflow = self._data.dtype.type(0.0)
    
  # In-place arithmetic operations
  @_match_rank
  def __iadd__(self, other):
    """self += someother"""
    if hasattr(other, "_data"):
      self._data += other._data
    else:
      self.data += other      
    return self
  
  @_match_rank
  def __isub__(self, other):
    """self -= someother"""
    if hasattr(other, "_data"):
      self._data -= other._data
    else:
      self.data -= other
    return self

  @_match_rank
  def __imul__(self, other):
    """self *= someother"""
    if hasattr(other, "_data"):
      self._data *= other._data
    else:
      self.data *= other
    return self
  
  @_match_rank
  def __idiv__(self, other):
    """self /= someother"""
    if hasattr(other, "_data"):
      self._data /= other._data
    else:
      self.data /= other
    return self
  
  @_match_rank
  def __ifloordiv__(self, other):
    """self //= someother"""
    if hasattr(other, "_data"):
      self._data //= other._data
    else:
      self.data //= other
    return self
  
  # Arithmetic operations
  def __add__(self, other):
    "self + other"
    new = copy.deepcopy(self)
    new += other
    return new
  
  def __sub__(self, other):
    "self - other"
    new = copy.deepcopy(self)
    new -= other
    return new

  def __mul__(self, other):
    "self * other"
    new = copy.deepcopy(self)
    new *= other
    return new

  def __div__(self, other):
    "self / other"
    new = copy.deepcopy(self)
    new /= other
    return new
  
  # Reverse arithmetic operations
  __radd__ = __add__

  def fill(self, value, weight=1.0):
    "Fills a bin in the histogram with the value and given weight"

    # Test for underflow
    if value < self._bins[0]:
      self.underflow += weight
      return
    # And test for overflow
    if value >= self._bins[-1]:
      self.overflow += weight
      return
    
    # Find the bin
    for (num, lowedge) in enumerate(self._bins[:-1]):
      if value >= lowedge and value < self._bins[num+1]:
        # We have found the bin!
        self._data[num] += weight
        return
    
    # Don't fail silently if we didn't find anything
    raise RuntimeError("Failed to find appropriate bin for value {0}".format(value))
  
  def __getitem__(self, key):
    return self._data[key]
  
  def __setitem__(self, key, value):
    return self._data.__setitem__(key, value)

  def __repr__(self):
    """Returns the representation"""
    return "Hist({bins},data={data})".format(bins=repr(self.bins), data=repr(self.data))

  def draw_hist(self, **kwargs):
    """Draw the histogram using matplotlib.
    
    Returns the matplotlib hist return values"""
    
    # Default to step type, if none has been declared
    if not kwargs.has_key("histtype"):
      kwargs["histtype"] = 'step'
    # Lazy import as it can take a little time to load and we might not always need to plot
    import matplotlib.pyplot as plt
    
    bins = binning.BinningScheme(self.bins)
    # Do the actual matplotlib drawing
    plot = plt.hist(bins.centers, weights=self.data, bins=self.bins, **kwargs)
    return plot

def fromTH1(hist):
  """Creates a hist object from a pyROOT TH1 object"""
  binedges = []
  bincontents = []
  bincount = hist.GetNbinsX()
  # Grab the bin values
  for bin in range(1,bincount+2):
    binedges.append(hist.GetBinLowEdge(bin))

  # Grab the data values separately
  for bin in range(1,bincount+1):
    bincontents.append(hist.GetBinContent(bin))
  
  # Grab the overflow and underflow
  overflow = hist.GetBinContent(bincount+1)
  underflow = hist.GetBinContent(0)

  # Build the new histogram
  newh = Hist(binedges, data=bincontents)
  newh.overflow = overflow
  newh.underflow = underflow
  return newh
