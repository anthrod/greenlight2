
import sys
import os

commonstocks_ratios_cachedir_name   = os.path.join("stocks","ratios")

def get_DE(symbol, cache_dir):
  ratios_dir = os.path.join(cache_dir, commonstocks_ratios_cachedir_name)
  file_path = os.path.join(ratios_dir, symbol + ".txt")
  if not os.path.exists(file_path):
    print("Could not open file: " + file_path)
    quit()
  DE = []
  with open(file_path, "r") as financials_file:
    for line in financials_file:
      if "Debt/Equity" in line:
        DE = line.strip("Debt/Equity,").strip("\n").split(",")
  if len(DE)==0:
    print("An error occured in reading Debt/Equity")
    quit()
  if '' in DE:
    print("Found blank entry in data. Replacing with mean")
    DE_nums = [float(x) for x in DE if x!='']
    nums_mean = sum(DE_nums) / len(DE_nums)
    for i in range(0,len(DE)):
      if DE[i]=='': DE[i] = nums_mean
  return DE
