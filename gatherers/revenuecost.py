
from indicator import IndicatorGatherer
import sys
import os

commonstocks_income_cachedir_name   = os.path.join("stocks","income")

class RevenueCostGatherer(IndicatorGatherer):

  def datadir(self):
    return os.path.join(self.cachedir, commonstocks_income_cachedir_name)

  def fetchentry(self, symbol):
    file_path = os.path.join(self.datadir(), symbol + ".txt")
    if not os.path.exists(file_path):
      print("Could not open file: " + file_path)
      quit()
    cost = []
    with open(file_path, "r") as financials_file:
      for line in financials_file:
        if "Cost of revenue" in line:
          cost = line.strip("Cost of revenue,").strip("\n").split(",")
          return cost
    print("Error: Could not retrieve cost of revenue for symbol " + symbol)
    return cost
