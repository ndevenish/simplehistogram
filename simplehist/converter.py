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
    return Hist(hist.bins, data=hist.data)
  else:
    # Look up in the type converter
    names = [x.__module__ + "." + x.__name__ for x in itertools.chain(type(hist).__bases__, [type(hist)])]
    converters = [x for x in _type_registry.keys() if x in names]
    if not converters:
      raise RuntimeError("Do not know how to convert object {}".format(type(hist)))
    return _type_registry[converters[-1]](hist)


def converts_type(typename):
  def _wrap(fn):
    _type_registry[typename] = fn
    def _decorate(*args, **kwargs):
      fn(*args, **kwargs)
    return _decorate
  return _wrap

@converts_type('ROOT.TH1')
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
