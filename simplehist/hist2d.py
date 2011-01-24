
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
    self.bins = (xbins, ybins)
    
    self._data = numpy.zeros((len(xbins)-1,len(ybins)-1))
    
  @property
  def bins(self):
    return self._bins
    
  @bins.setter
  def bins(self, value):
    if len(value) != 2:
      raise BinError("Must provide two dimensions of bin boundaries")
    
    # Pass through the arrays inside value as a tuple array
    self._bins = BinTuple(*(tuple(x) for x in value))
  
  @property
  def rank(self):
    """Returns the dimensionality of the histogram"""
    return 2
  
  @property
  def data(self):
    return self._data