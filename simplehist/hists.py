# coding: utf-8

"""
hists.py

Copyright (c) 2014 Nicholas Devenish <n.e.devenish@sussex.ac.uk>

An easy, quick, lightweight histogram class based on ndarray

Initialise with bin indices:
  >>> a = Hist([0, 1, 2, 3])
  >>> len(a)
  3
  >>> a.bins
  array([0, 1, 2, 3])

Optionally include data:
  >>> Hist([0, 1, 2, 3], data=[1, 0.2, 3])
  Hist([0, 1, 2, 3], data=[ 1. ,  0.2,  3. ])

Or just specify the blank data type:
  >>> a = Hist([0, 1, 2, 3], dtype=int)
  >>> a
  Hist([0, 1, 2, 3], data=[0, 0, 0])

You can do any normal numpy arithmetic operations:
  >>> a = Hist([0, 1, 2, 3], data=[1, 0.2, 3])
  >>> b = a + a
  >>> b -= a
  >>> all(a == b)
  True

And you can fill bins from values:
  >>> a = Hist([0,1,2,3])
  >>> a.fill(1.4, 3)
  >>> a
  Hist([0, 1, 2, 3], data=[ 0.,  3.,  0.])

Or from arrays:
  >>> a = Hist([0,1,2,3])
  >>> a.fill([1.4, 2.4], weights=[1, 2])
  >>> a
  Hist([0, 1, 2, 3], data=[ 0.,  1.,  2.])

If you use pyROOT, you can convert from 1D histograms:
  >>> type(source)
  <class 'ROOT.TH1D'>
  >>> convert = ashist(source)
  >>> type(convert)
  <class 'simplehist.hists.Hist'>

Or conversion from custom types - see simplehist.converter for
implementation details.

You can also draw histograms, using any of the options
that can be passed to matplotlib.pyplot.plot:
  >>> hist_object.draw_hist(lw=2)
"""

import sys
import numpy

# A numpy array with bins, and constraints on those bins
class Hist(numpy.ndarray):
  def __new__(cls, bins, data=None, **kwargs):
    # If bins contains items that are list-like then it is probably multidim
    if isinstance(bins[0], (tuple, list)):
      # It must be multi-dimension...
      bins = tuple(numpy.asarray(x) for x in bins)
      ndims = len(bins)
      shape = tuple(len(x)-1 for x in bins)
    else:
      # Just a single dimension
      bins = numpy.asarray(bins)
      assert bins.ndim == 1
      ndims = 1
      shape = (len(bins)-1,)

    # Create or validate the data shape
    if data is None:
      # data = numpy.zeros(tuple(x-1 for x in bins.shape), **kwargs)
      data = numpy.zeros(shape, **kwargs)
    else:
      data = numpy.asarray(data, **kwargs)
      # Same dimensions and shape-1
      assert ndims == data.ndim
      if ndims == 1:
        assert all(x == len(y)-1 for x, y in zip(data.shape, [bins]))
      else:
        assert all(x == len(y)-1 for x, y in zip(data.shape, bins))

    # Cast from our data array
    obj = data.view(cls)
    obj._bins = bins
    return obj

  def __array_finalize__(self, obj):
    # Since always creating as an alternate, this should never happen
    assert obj is not None
    # Other should always have a _bins object
    self._bins = getattr(obj,"_bins",None)

  def __array_wrap__(self,obj,context=None):
    # if obj.ndim == 0 and obj.size == 1:
    #   return obj.item()
    # Don't wrap as a hist if the shape changed - we have no idea how it did so
    if not obj.shape == self.shape:
      return obj
    return super(Hist,self).__array_wrap__(obj,context)

  @property
  def bins(self):
      return self._bins
  @bins.setter
  def bins(self, value):
    value = numpy.asarray(value)
    assert value.ndim == self.ndim
    assert all(x == y-1 for x, y in zip(self.shape, value.shape))
    self._bins = value

  def __getitem__(self, index):
    """Return a value, or a subhist from a slice.

    Getting singular indices just returns the values, whilst slices return
    subhists, with applicable bins."""

    return super(Hist, self).__getitem__(index)

    if isinstance(index, tuple) and self.ndim == 1:
      binSel = []
      # Build a new tuple for each of the entries
      for selection in index:
        if selection is Ellipsis:
          binSel.append(Ellipsis)
        elif isinstance(selection, slice):
          # Stepping really doesn't make much sense with bins
          assert selection.step is None or selection.step == 1
          if selection.stop is not None:
            binSel.append(slice(selection.start, min(sys.maxint,selection.stop+1)))
          else:
            binSel.append(slice(selection.start, None))
        elif isinstance(selection, int):
          binSel.append(slice(selection, selection+1))
        else:
          # Throw away the hist information as we don't understand the request
          return super(Hist, self).__getitem__(index).view(numpy.ndarray)
          #assert False
      # Build a new histogram with these bins
      ret = super(Hist,self).__getitem__(index).view(Hist)
      # If this gave us a hist.. 
      if hasattr(ret, "_bins"):
        ret._bins = self._bins.__getitem__(tuple(binSel))
      return ret
  
    else:
      return super(Hist, self).__getitem__(index)

  def __getslice__(self, i, j):
    return self.__getitem__((slice(i,j),))

  def __repr__(self):
    # if numpy.all(self == 0):
    #   # Bin-only output
    #   return "{}(bins={})".format(type(self).__name__, numpy.array_repr(self._bins))
    # else:
    if self.ndim == 1:
      return "{}({}, data={})".format(type(self).__name__,
        numpy.array_repr(self._bins)[len("array("):-1], 
        numpy.array_repr(self)[len(type(self).__name__)+1:-1])
    else:
      return "{}(({}), data={})".format(type(self).__name__,
        ",".join([numpy.array_repr(x)[6:-1] for x in self._bins]), 
        numpy.array_repr(self)[len(type(self).__name__)+1:-1])

  def fill(self, values, weights=None):
    values = numpy.asarray(values)
    if weights is not None:
      weights = numpy.asarray(weights)
    else:
      weights = numpy.ones(values.shape)
    assert values.shape == weights.shape

    # Promote scalars, if required
    if values.ndim == 0:
      values = values[numpy.newaxis]
      weights = weights[numpy.newaxis]
    bins = numpy.digitize(values, self._bins)
    newValues = numpy.zeros(self.shape)
    # Now fill all the bins
    for _bin, weight in zip(bins, weights):
      if _bin < 1 or _bin > len(newValues):
        continue
      newValues[_bin-1] += weight
    # add to the current instance
    self += newValues

  def draw_hist(self, **kwargs):
    assert self.ndim == 1
    import matplotlib.pyplot as plt
    x = numpy.zeros(len(self)*2)
    x[0::2] = self.bins[:-1]
    x[1::2] = self.bins[1:]
    y = numpy.array(numpy.repeat(self,2))
    # import pdb
    # pdb.set_trace()

    return plt.plot(x,y,**kwargs)

  def pcolor(self, *args, **kwargs):
    assert self.ndim == 2
    import matplotlib.pyplot as plt
    plt.pcolor(self.bins[0], self.bins[1], self.T, *args, **kwargs)

  def pcolormesh(self, *args, **kwargs):
    assert self.ndim == 2
    import matplotlib.pyplot as plt
    plt.pcolor(self.bins[0], self.bins[1], self.T, *args, **kwargs)