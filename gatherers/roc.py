
from indicator import IndicatorGatherer
import sys
import os

commonstocks_ratios_cachedir_name   = os.path.join("stocks","ratios")

class ROCGatherer(IndicatorGatherer):

  def datadir(self):
    return os.path.join(self.cachedir, commonstocks_ratios_cachedir_name)

  def fetchentry(self, symbol):
    file_path = os.path.join(self.datadir(), symbol + ".txt")
    if not os.path.exists(file_path):
      print("Could not open file: " + file_path)
      quit()
    ROC = []
    with open(file_path, "r") as financials_file:
      for line in financials_file:
        if "Profitability" in line:
          num_years = len(line.split(","))-1
        if "Return on Invested Capital" in line:
          ROC = line.strip("Return on Invested Capital %,").strip("\n").split(",")
          return ROC
    print("Error: Could not retrieve ROC for symbol " + symbol)
    quit()
