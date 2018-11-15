

from indicator import IndicatorGatherer
from roa import ROAGatherer
import sys
import os

commonstocks_ratios_cachedir_name   = os.path.join("stocks","ratios")

class ROA8YrGatherer(ROAGatherer):

  def postprocessdata(self):
    super(ROA8YrGatherer, self).postprocessdata()
    for item in self.datadict.items():
      ROAs = item[1]
      if not len(ROAs)>=8:
        print("Error: Could not retrieve at least 8 years of ROA data for symbol " + symbol)
        quit()
      ROAs.reverse()
      ROA8 = [1.0]
      for i in range(0,8):
        ROA8[0] *= (1.0 + float(ROAs[i])/100.0)
      if ROA8[0]<=0.0: self.datadict[item[0]] = [0.0]
      else: self.datadict[item[0]] = [100*(pow(ROA8[0], 1.0/8.0) - 1)]
