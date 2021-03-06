
from indicator import IndicatorGatherer
import sys
import os

commonstocks_ratios_cachedir_name   = os.path.join("stocks","ratios")

class EPSGatherer(IndicatorGatherer):
  def datadir(self):
    return os.path.join(self.cachedir, commonstocks_ratios_cachedir_name)

  def fetchentry(self, symbol):
    file_path = os.path.join(self.datadir(), symbol + ".txt")
    if not os.path.exists(file_path):
      print("Could not open file: " + file_path)
      quit()
    with open(file_path, "r") as financials_file:
      for line in financials_file:
        if "EPS %" in line:
          return financials_file.next().strip("Year over Year,,").strip("\n").split(",")
    print("Error: Could not retrieve EPS for symbol " + symbol)
    quit() 
