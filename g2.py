
import os
from datetime import datetime
import argparse

from hunters.symbols import snp500
from hunters.timeseries import stocks
from hunters.financials import morningstar

snp500_symbols_filename = "snp500_symbols.txt"
cache_varname = "GREENLIGHT_CACHE_PATH"
timestamp_file_name = "data_timestamp.txt"

def checkCachePath():
  if not cache_varname in os.environ:
    print("Error: Cannot find cache path variable \"" + cache_varname + "\" in environment")
    quit()
  if not os.path.isdir(os.environ[cache_varname]):
    print("Error: Could not find a directory at specified path \"" + os.environ[cache_varname] + "\"")
    quit()
  print("Using Cache Path: \"" + os.environ[cache_varname] + "\"")

def doUpdates():
  print("Updating S&P500 symbols...")
  snp500.update_snp500_symbols( os.environ[cache_varname] )  
  print("Pulling S&P500 time series data...")
  if not os.path.exists(os.path.join(os.environ[cache_varname], "stocks")):
    os.mkdir (os.path.join(os.environ[cache_varname], "stocks"))
  stocks.fetch_timeseries() 
  morningstar.pull_financials( os.environ[cache_varname] )
  print("Pulling financial data") 

if __name__ == '__main__':
  parser = argparse.ArgumentParser(description="See numbers. Burn money.")
  parser.add_argument("--update", "-u", dest="doUpdate", default=False, action="store_true")
  args = parser.parse_args()
  checkCachePath()
  if (args.doUpdate):
    doUpdates()







