# coding: utf-8

"""
hists.py

Created by Nicholas Devenish on 2011-01-12.

An easy, quick, lightweight histogram class based on ndarray

Initialise with bin indices:
  >>> a = Hist([0, 1, 2, 3])
  >>> a.bincount
  3
  >>> a.bins
  (0, 1, 2, 3)
  >>> a.data
  array([ 0.,  0.,  0.])

Optionally include data and optional dtype:
  >>> a = Hist([0, 1, 2, 3], data=[1, 0.2, 3], dtype=float)
  >>> a.data
  array([ 1. ,  0.2,  3. ])

You can do arithmetic operations in place or seperately:
  >>> a = Hist([0, 1, 2, 3], data=[1, 0.2, 3])
  >>> b = a + a
  >>> b -= a
  >>> a.data == b.data
  array([ True,  True,  True], dtype=bool)  
  
"""


import numpy
import copy

class BinError(Exception):
  pass

def _match_rank(f):
  """Decorator to ensure that the second argument matches rank"""
  def checkrank(self, other):
    if isinstance(other, Hist):
      if self.data.size != other.data.size:
        raise TypeError("Histogram data arrays do not match size! {} != {}"
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
      self.data = numpy.zeros(len(bins)-1, dtype=dtype)
    else:
      self.data = numpy.array(data)

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
    
    # Ensure the bins are numerically sequential
    if not tuple(newbins) == tuple(sorted(newbins)):
      raise BinError("Bins must be numerically ascending")
    
    # Do we need to resize our data?
    if self._bins and len(newbins) != len(self._bins):
      self.data.resize(len(newbins)-1)
    
    self._bins = tuple(newbins)
  
  @property
  def bincount(self):
    "Returns the number of bins"
    return self.data.size
  
  @property
  def data(self):
    "Returns the data object"
    return self._data
  
  @data.setter
  def data(self, newdata):
    "Sets the internal data object"
    # Check this matches our bin count
    if len(newdata) == len(self._bins)-1:
      self._data = numpy.array(newdata)
    else:
      raise BinError("Data incorrect dimensions! Data size {} != {} bins".format(len(newdata), len(self._bins)-1))
  
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
