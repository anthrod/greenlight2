
import os
from datetime import datetime
import argparse
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import lognorm

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
  parser.add_argument("--histROC", dest="histROC", default=False, action="store_true")
  args = parser.parse_args()
  checkCachePath()
  if (args.doUpdate):
    doUpdates()
  if (args.plotDE is not None):
    if (args.plotDE=="all"):
      datadict = de.get_all_DE(os.environ[cache_varname])
      for data in datadict.items():
        plt.plot(data[1])
    else:
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
    if (args.plotROC=="all"):
      datadict = roc.get_all_ROC(os.environ[cache_varname])
      for data in datadict.items():
        plt.plot(data[1])
    else:
      data = roc.get_ROC(args.plotROC, os.environ[cache_varname]) 
      print(data)
      plt.plot(data)
    plt.ylabel("Return on Capital (%)")
    plt.show()
  if (args.histROC==True):
    data = roc.get_all_current_ROC(os.environ[cache_varname])
    hist_data = []
    for item in data.items():
      if (float(item[1]) > 0):
        hist_data.append(float(item[1]))
    data = sorted(data.items(), key=lambda kv:kv[1])
    for item in data: print(item)
    bins = np.arange(min(hist_data), max(hist_data), 2)
    ax1 = plt.subplot(211)
    plt.title('Return on Investment Capital (Positive returns only)')
    plt.xlim([0, max(hist_data)])
    ax1.hist(hist_data, bins=bins, normed=True, alpha=0.8)
    shape, loc, scale = lognorm.fit(hist_data)
    pdf = lognorm.pdf(bins,shape,loc,scale)
    ax1.plot(bins,pdf,'r')
    ax2 = plt.subplot(212)
    cdf = lognorm.cdf(bins,shape,loc,scale)
    ax2.plot(bins,cdf,'r')
    plt.show() 





