
import os
from datetime import datetime
import argparse
import matplotlib.pyplot as plt

from hunters.symbols import snp500
from hunters.timeseries import stocks
from hunters.financials import morningstar
from gatherers import de
from gatherers import eps
from gatherers import roc

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
  parser.add_argument("--plotDE", dest="plotDE", default=None)
  parser.add_argument("--plotEPS", dest="plotEPS", default=None)
  parser.add_argument("--plotROC", dest="plotROC", default=None)
  args = parser.parse_args()
  checkCachePath()
  if (args.doUpdate):
    doUpdates()
  if (args.plotDE is not None):
    data = de.get_DE(args.plotDE, os.environ[cache_varname]) 
    plt.plot(data)
    plt.ylabel("Debt to Equity Ratio")
    plt.show()
  if (args.plotEPS is not None):
    data = eps.get_EPS(args.plotEPS, os.environ[cache_varname]) 
    plt.plot(data)
    plt.ylabel("Earnings Per Share")
    plt.show()
  if (args.plotROC is not None):
    data = roc.get_ROC(args.plotROC, os.environ[cache_varname]) 
    plt.plot(data)
    plt.ylabel("Return on Capital (%)")
    plt.show()







