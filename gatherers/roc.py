
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

def get_current_ROC(symbol, cache_dir):
  ROC_history = get_ROC(symbol, cache_dir)
  if len(ROC_history)>0:
    ROC_history = ROC_history[-1]
  return ROC_history

def get_all_ROC(cache_dir):
  ratios_dir = os.path.join(cache_dir, commonstocks_ratios_cachedir_name)
  all_files = os.listdir(ratios_dir)
  roc_dict = {}
  maxdatasize = 0
  for ratiosfile in all_files:
    symbol = ratiosfile.strip(".txt")
    data = get_ROC(symbol,cache_dir) 
    if len(data)>0 and not '' in data:
      data = [float(x) for x in data]
      maxdatasize = max(len(data),maxdatasize)
      roc_dict[symbol] = data
  for i in roc_dict.items():
    missing_data  = [0]*(maxdatasize - len(i[1]))
    missing_data += i[1]
    roc_dict[i[0]] = missing_data
  return roc_dict

def get_all_current_ROC(cache_dir):
  ratios_dir = os.path.join(cache_dir, commonstocks_ratios_cachedir_name)
  all_files = os.listdir(ratios_dir)
  roc_dict = {}
  maxdatasize = 0
  for ratiosfile in all_files:
    symbol = ratiosfile.strip(".txt")
    data = get_current_ROC(symbol,cache_dir) 
    if len(data)>0:
      roc_dict[symbol] = data
  return roc_dict
