
from indicator import IndicatorGatherer
import revenue
import revenuecost
import totalassets
import sys
import os

commonstocks_income_cachedir_name   = os.path.join("stocks","income")

class GPAGatherer(IndicatorGatherer):

  def datadir(self):
    return os.path.join(self.cachedir, commonstocks_income_cachedir_name)

  def fetchentry(self, symbol):
    file_path = os.path.join(self.datadir(), symbol + ".txt")

    R = revenue.RevenueGatherer(symbol, self.cachedir)
    COR = revenuecost.RevenueCostGatherer(symbol, self.cachedir)
    TA = totalassets.TotalAssetsGatherer(symbol, self.cachedir)

    if symbol in R.datadict:
      R = R.datadict[symbol]
    else:
      print("Invalid revenue: " + symbol)
      return []

    if symbol in COR.datadict:
      COR = COR.datadict[symbol]
    else:
      print("Invalid Cost of Revenue: " + symbol)
      return []

    if symbol in TA.datadict:
      TA = TA.datadict[symbol]
    else:
      print("Invalid Total Assets: " + symbol)
      return []  

    if R==[] or COR==[] or TA==[]: return [0]

    if not (len(R)==len(COR) and len(COR)==len(TA)+1):
      print("Error: Revenue length " + str(len(R)) + ", Revenue Cost length " + str(len(COR)) + ", Total Assets length " + str(len(TA)))
      print("Invalid values for symbol " + symbol)
      return [0]

    gpa = []
    #Use length of TA here because there is no TTM for TA
    for i in range(0,len(TA)):
      gpa.append(  ( float(R[i]) - float(COR[i]) ) / float(TA[i]) )
    return gpa
