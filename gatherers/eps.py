
import sys
import os

commonstocks_ratios_cachedir_name   = os.path.join("stocks","ratios")

def get_EPS(symbol, cache_dir):
  ratios_dir = os.path.join(cache_dir, commonstocks_ratios_cachedir_name)
  file_path = os.path.join(ratios_dir, symbol + ".txt")
  if not os.path.exists(file_path):
    print("Could not open file: " + file_path)
    quit()
  EPS = []
  with open(file_path, "r") as financials_file:
    for line in financials_file:
      if "EPS %" in line:
        EPS = financials_file.next().strip("Year over Year,,").strip("\n").split(",")
  if len(EPS)==0:
    print("An error occured in reading Earnings Per Share")
    quit()
  return EPS
