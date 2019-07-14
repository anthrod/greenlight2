
from indicator import IndicatorGatherer
import sys
import os

commonstocks_balance_cachedir_name = os.path.join("stocks","balance")

class OperatingAssetsGatherer(IndicatorGatherer):

  def datadir(self):
    return os.path.join(self.cachedir, commonstocks_balance_cachedir_name)

  def fetchentry(self, symbol):
    file_path = os.path.join(self.datadir(), symbol + ".txt")
    if not os.path.exists(file_path):
      print("Could not open file: " + file_path)
      quit()
    assets = []
    with open(file_path, "r") as financials_file:
      for line in financials_file:
        if "Total current assets" in line:
          assets = line.strip("Total current assets,").strip("\n").split(",")
          return assets
    print("Error: Could not retrieve operating [current] assets for symbol " + symbol)
    return assets
