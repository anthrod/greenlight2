
import sys
import os

commonstocks_ratios_cachedir_name   = os.path.join("stocks","ratios")

def get_ROC(symbol, cache_dir):
  ratios_dir = os.path.join(cache_dir, commonstocks_ratios_cachedir_name)
  file_path = os.path.join(ratios_dir, symbol + ".txt")
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
