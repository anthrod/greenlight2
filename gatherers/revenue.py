
from indicator import IndicatorGatherer
import sys
import os

commonstocks_income_cachedir_name   = os.path.join("stocks","income")

class RevenueGatherer(IndicatorGatherer):

  def datadir(self):
    return os.path.join(self.cachedir, commonstocks_income_cachedir_name)

  def fetchentry(self, symbol):
    file_path = os.path.join(self.datadir(), symbol + ".txt")
    if not os.path.exists(file_path):
      print("Could not open file: " + file_path)
      quit()
    revenue = []
    with open(file_path, "r") as financials_file:
      for line in financials_file:
        if "Revenue," in line:
          revenue = line.strip("Revenue,").strip("\n").split(",")
          return revenue
        elif "Total revenues," in line:
          revenue = line.strip("Total revenues,").strip("\n").split(",")
          return revenue
    print("Error: Could not retrieve revenue for symbol " + symbol)
    return revenue
