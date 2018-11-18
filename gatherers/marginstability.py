

from indicator import IndicatorGatherer
from grossmargin import GrossMarginGatherer
import numpy as np
import sys
import os

commonstocks_ratios_cachedir_name   = os.path.join("stocks","ratios")

class MarginStabilityGatherer(GrossMarginGatherer):

  def postprocessdata(self):
    super(MarginStabilityGatherer, self).postprocessdata()
    for item in self.datadict.items():
      GMs = item[1]
      if not len(GMs)>=8:
        print("Error: Could not retrieve at least 8 years of Gross Margin data for symbol " + symbol)
        quit()
      indices_to_delete = len(GMs)-8
      GMs.reverse()
      for i in range(0,indices_to_delete):
        GMs.pop()
      GMs.reverse()
      GMs = np.array(GMs)
      self.datadict[item[0]] = [np.mean(GMs)/np.std(GMs)]
