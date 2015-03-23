# coding: utf-8

"""Contains code for converting from other histogram types, and hooking
into this system so that additional type converters can be added."""

import itertools
from .hists import Hist

_type_registry = {}

def ashist(hist, copy=True):
  """Converts from an input object to a Hist histogram"""
  if isinstance(hist, Hist) and not copy:
    return hist
  if isinstance(hist, Hist):
    return Hist(hist.bins, data=hist)
  else:
    # Look up in the type converter
    names = [x.__module__ + "." + x.__name__ for x in itertools.chain(type(hist).__bases__, [type(hist)])]
    converters = []
    for key, converter in _type_registry.items():
      if callable(key):
        if not key(hist):
          continue
      else:
        if not key in names:
          continue
      converters.append(converter)

    #converters = [x for x in _type_registry.keys() if x in names]
    if not converters:
      raise RuntimeError("Do not know how to convert object {}".format(type(hist)))
    return converters[-1](hist)


def converts_type(typename):
  def _wrap(fn):
    _type_registry[typename] = fn
    def _decorate(*args, **kwargs):
      fn(*args, **kwargs)
    return _decorate
  return _wrap

# @converts_type('ROOT.TH1')
# @converts_type('__main__.TH1')
@converts_type(lambda x: hasattr(x, "ClassName") and x.ClassName().startswith("TH1"))
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

@converts_type(lambda x: hasattr(x, "ClassName") and x.ClassName().startswith("TH2"))
def fromTH2(hist):
  """Convert a TH2 histogram"""
  bincount = (hist.GetNbinsX(), hist.GetNbinsY())
  binedges = ([hist.GetXaxis().GetBinLowEdge(x) for x in range(1,bincount[0]+2)],
              [hist.GetYaxis().GetBinLowEdge(x) for x in range(1,bincount[1]+2)])

  h = Hist(binedges)

  for xbin in range(1,bincount[0]+1):
    for ybin in range(1,bincount[1]+1):
      h[xbin-1,ybin-1] = hist.GetBinContent(xbin,ybin)

  import numpy as np
  import matplotlib.pyplot as plt
  
  import pdb
  pdb.set_trace()
  return h