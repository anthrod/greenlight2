
from indicator import IndicatorGatherer
import sys
import os

commonstocks_ratios_cachedir_name   = os.path.join("stocks","ratios")

class DEGatherer(IndicatorGatherer):
  def datadir(self):
    return os.path.join(self.cachedir, commonstocks_ratios_cachedir_name)

  def fetchentry(self, symbol):
    file_path = os.path.join(self.datadir(), symbol + ".txt")
    if not os.path.exists(file_path):
      print("Could not open file: " + file_path)
      quit()
    DE = []
    with open(file_path, "r") as financials_file:
      for line in financials_file:
        if "Debt/Equity" in line:
          DE = line.strip("Debt/Equity,").strip("\n").split(",")
          return DE
    print("Error: Could not retrieve DE for symbol " + symbol)
    quit()

