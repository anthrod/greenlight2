

from indicator import IndicatorGatherer
from roc import ROCGatherer
import sys
import os

commonstocks_ratios_cachedir_name   = os.path.join("stocks","ratios")

class ROC8YrGatherer(ROCGatherer):

  def postprocessdata(self):
    super(ROC8YrGatherer, self).postprocessdata()
    for item in self.datadict.items():
      ROCs = item[1]
      if not len(ROCs)>=8:
        print("Error: Could not retrieve at least 8 years of ROC data for symbol " + symbol)
        quit()
      ROCs.reverse()
      ROC8 = [1.0]
      for i in range(0,8):
        ROC8[0] *= (1.0 + float(ROCs[i])/100.0)
      if ROC8[0]<=0.0: self.datadict[item[0]] = [0.0]
      else: self.datadict[item[0]] = [ 100*(pow(ROC8[0], 1.0/8.0) - 1) ]
