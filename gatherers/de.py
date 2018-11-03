
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
    print("An error occured in reading Debt/Equity for symbol " + symbol)
  elif '' in DE:
    print("Found blank entry in data. Replacing with mean")
    DE_nums = [float(x) for x in DE if x!='']
    if sum(DE_nums) == 0:
      return []
    nums_mean = sum(DE_nums) / len(DE_nums)
    for i in range(0,len(DE)):
      if DE[i]=='': DE[i] = nums_mean
  return DE

def get_current_DE(symbol, cache_dir):
  DE_history = get_DE(symbol, cache_dir)
  if len(DE_history)>0:
    DE_history = DE_history[-1]
  return DE_history

def get_all_DE(cache_dir):
  ratios_dir = os.path.join(cache_dir, commonstocks_ratios_cachedir_name)
  all_files = os.listdir(ratios_dir)
  de_dict = {}
  maxdatasize = 0
  for ratiosfile in all_files:
    symbol = ratiosfile.strip(".txt")
    data = get_DE(symbol,cache_dir) 
    if len(data)>0 and not '' in data:
      data = [float(x) for x in data]
      maxdatasize = max(len(data),maxdatasize)
      de_dict[symbol] = data
  for i in de_dict.items():
    missing_data  = [0]*(maxdatasize - len(i[1]))
    missing_data += i[1]
    de_dict[i[0]] = missing_data
  return de_dict

def get_all_current_DE(cache_dir):
  ratios_dir = os.path.join(cache_dir, commonstocks_ratios_cachedir_name)
  all_files = os.listdir(ratios_dir)
  de_dict = {}
  maxdatasize = 0
  for ratiosfile in all_files:
    symbol = ratiosfile.strip(".txt")
    data = get_current_DE(symbol,cache_dir) 
    if len(data)>0:
      de_dict[symbol] = data
  return de_dict
