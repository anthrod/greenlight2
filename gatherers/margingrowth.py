

from indicator import IndicatorGatherer
from grossmargin import GrossMarginGatherer
import sys
import os

commonstocks_ratios_cachedir_name   = os.path.join("stocks","ratios")

class MarginGrowthGatherer(GrossMarginGatherer):

  def postprocessdata(self):
    super(MarginGrowthGatherer, self).postprocessdata()
    for item in self.datadict.items():
      GMs = item[1]
      if not len(GMs)>=8:
        print("Error: Could not retrieve at least 8 years of ROA data for symbol " + symbol)
        quit()
      indices_to_delete = len(GMs)-8
      GMs.reverse()
      for i in range(0,indices_to_delete):
        GMs.pop()
      GMs.reverse()
      MG = [1.0]
      for gm in GMs:
        if float(gm)<1e-6:
          print("Warning: Could not interpret growth value: " + str(gm))
          self.datadict[item[0]] = [0.0]
          return
      for i in range(1,8):
        MG[0] *= (1.0 + float(GMs[i])/float(GMs[i-1]))
      if MG[0]<=0.0: self.datadict[item[0]] = [0.0]
      else: self.datadict[item[0]] = [100*(pow(MG[0], 1.0/7.0) - 1)]
