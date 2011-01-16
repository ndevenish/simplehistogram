# coding: utf-8

"""
bins.py

Copyright (c) 2011 Nicholas Devenish <n.e.devenish@sussex.ac.uk>

Contains the logic for creating and inspecting sequences of bins
"""

__license__ = """Copyright (c) 2011 Nicholas Devenish <n.e.devenish@sussex.ac.uk>
MIT License <http://www.opensource.org/licenses/mit-license.php>
"""

import numpy

class BinError(Exception):
  pass

# class Bin(object):
#   """Represents a single bin"""
#   def __init__(self, lowedge, highedge):
#     self.lowedge = lowedge
#     self.highedge = highedge
#     self.width = highedge - lowedge
#     self.center = lowedge + width/2.

class BinningScheme(object):
  """Holds all the information on a particular scheme of binning, for one axis"""
  def __init__(self, binarray):
    """Create a binning scheme from a source set of bins"""
    
    if len(binarray) == 1:
      raise BinError("Must provide more that one value for a single bin")
      
    # Calculate the number of bins
    if len(binarray) == 0:
      bincount = 0
    else:
      bincount = len(binarray)-1
    
    # Ensure the bins are numerically sequential
    if not tuple(binarray) == tuple(sorted(binarray)):
      raise BinError("Bins must be numerically ascending")
    
    self._bintuple = tuple(binarray)
  
  def __len__(self):
    if len(self._bintuple) is 0:
      return 0
    return len(self._bintuple)-1
  
  def __getitem__(self, key):
    return self._bintuple[key]
  
  @property
  def centers(self):
    """Returns the bin centers for every bin"""
    vals = []
    for i, low in enumerate(self._bintuple[:-1]):
      high = self._bintuple[i+1]
      vals.append(low + (high-low)/2.)
    return tuple(vals)
  
  @property
  def lowedges(self):
    """Returns the bin lower edges"""
    return self._bintuple[:-1]
  
  @property
  def edges(self):
    """Returns the bin lower edges"""
    return self._bintuple