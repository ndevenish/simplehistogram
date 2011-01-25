
import copy
from collections import namedtuple
import numpy


from binning import BinError
import binning

BinTuple = namedtuple('BinTuple','x y')

class Hist2D(object):
  """ndarray based 2D histogram object"""

  def __init__(self, xbins, ybins):
    """Initialise the 2D histogram object.
    
    xbins: The array of x bin edges
    ybins: The array of y bin edges
    """
    self._bins = None
    self.bins = (xbins, ybins)
    
    self._data = numpy.zeros((len(xbins)-1,len(ybins)-1))
    
  @property
  def bins(self):
    return self._bins
    
  @bins.setter
  def bins(self, value):
    """Sets the bin array. Resizes data if required."""
    
    # Make sure that we were passed the correct dimensionality of bins
    if len(value) != 2:
      raise BinError("Must provide two dimensions of bin boundaries")

    # Verify that all the passed in lists are valid
    for i, bins in enumerate(value):
      if len(bins) < 2:
        raise BinError("Bin dimension {0} must be >= 2 values".format(i))

    # Work out the bin size array
    newsize = tuple(len(x)-1 for x in value)
    
    # Do we need to resize our data array?
    if self._bins and newsize != self.bincount:
      self.data.resize(newsize)
    
    # Pass through the arrays inside value as a tuple array
    self._bins = BinTuple(*(tuple(x) for x in value))
    
  @property
  def bincount(self):
    "Returns the number of bins"
    return tuple(len(x)-1 for x in self.bins)
      
  @property
  def rank(self):
    """Returns the dimensionality of the histogram"""
    return 2
  
  @property
  def data(self):
    return self._data
  
  @data.setter
  def data(self, value):
    """Sets the data array"""
    
    numpyval = numpy.array(value)
    
    # Validate that the size matches our bin count
    if numpyval.shape != self.bincount:
      raise BinError("Data incorrect dimensions! Data size {0} != {1} bins".format(numpyval.shape, tuple(self.bincount)))
    
    self._data = numpyval

  def __getitem__(self, key):
    return self._data[key]

  def __setitem__(self, key, value):
    return self._data.__setitem__(key, value)