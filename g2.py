
import os
from datetime import datetime
import argparse
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import lognorm
from scipy.stats import norm

from hunters.symbols import snp500
from hunters.symbols import exchanges
from hunters.timeseries import stocks
from hunters.financials import morningstar
from gatherers import de
from gatherers import eps
from gatherers import roc
from gatherers import roc8yr
from gatherers import gpa

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
  print("Pulling symbol data for US exchanges...")
  exchanges.getsymbols( os.environ[cache_varname] )
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
  parser.add_argument("--histDE", dest="histDE", default=False, action="store_true")
  parser.add_argument("--plotEPS", dest="plotEPS", default=None)
  parser.add_argument("--histEPS", dest="histEPS", default=False, action="store_true")
  parser.add_argument("--plotROC", dest="plotROC", default=None)
  parser.add_argument("--histROC", dest="histROC", default=False, action="store_true")
  parser.add_argument("--histROC8", dest="histROC8", default=False, action="store_true")
  parser.add_argument("--plotGPA", dest="plotGPA", default=None)
  parser.add_argument("--histGPA", dest="histGPA", default=False, action="store_true")
  args = parser.parse_args()
  checkCachePath()
  if args.doUpdate:
    doUpdates()
  if args.plotDE is not None:
    gatherer = de.DEGatherer(args.plotDE, os.environ[cache_varname])
    for data in gatherer.datadict.items():
      plt.plot(data[1])
    plt.ylabel("Debt to Equity Ratio")
    plt.show()
  if args.histDE is True: 
    gatherer = de.DEGatherer("all", os.environ[cache_varname])
    data = gatherer.mostrecent()
    hist_data = []
    for item in data.items():
      hist_data.append(float(item[1]))
    data = sorted(data.items(), reverse=True, key=lambda kv:kv[1])
    for item in data: print(item)
    bins = np.arange(min(hist_data), max(hist_data), 0.1)
    ax1 = plt.subplot(211)
    plt.title('Ratio of debt to equity')
    plt.xlim([min(hist_data), max(hist_data)])
    ax1.hist(hist_data, bins=bins, normed=True, alpha=0.8)
    shape, loc, scale = lognorm.fit(hist_data)
    pdf = lognorm.pdf(bins,shape,loc,scale)
    ax1.plot(bins,pdf,'r')
    ax2 = plt.subplot(212)
    cdf = lognorm.cdf(bins,shape,loc,scale)
    ax2.plot(bins,cdf,'r')
    plt.show() 
  if args.plotEPS is not None:
    gatherer = eps.EPSGatherer(args.plotEPS, os.environ[cache_varname])
    for data in gatherer.datadict.items():
      plt.plot(data[1])
    plt.ylabel("Earnings Per Share")
    plt.show()
  if args.histEPS is True: 
    gatherer = eps.EPSGatherer("all", os.environ[cache_varname])
    data = gatherer.mostrecent()
    hist_data = []
    for item in data.items():
      hist_data.append(float(item[1]))
    data = sorted(data.items(), key=lambda kv:kv[1])
    for item in data: print(item)
    bins = np.arange(-400, 400, 10.0)
    ax1 = plt.subplot(211)
    plt.title('Earnings Per Share')
    plt.xlim([min(hist_data), max(hist_data)])
    ax1.hist(hist_data, bins=bins, normed=True, alpha=0.8)
    mu,std = norm.fit(hist_data)
    pdf = norm.pdf(bins,mu,std)
    ax1.plot(bins,pdf,'r')
    ax2 = plt.subplot(212)
    cdf = norm.cdf(bins,mu,std)
    ax2.plot(bins,cdf,'r')
    plt.show() 
  if (args.plotROC is not None):
    gatherer = roc.ROCGatherer(args.plotROC, os.environ[cache_varname])
    for data in gatherer.datadict.items():
      plt.plot(data[1])
    plt.ylabel("Return on Capital (%)")
    plt.show()
  if (args.histROC==True):
    gatherer = roc.ROCGatherer("all", os.environ[cache_varname])
    data = gatherer.mostrecent()
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
  if args.histROC8:
    gatherer = roc8yr.ROC8YrGatherer("all", os.environ[cache_varname])
    data = gatherer.mostrecent()
    hist_data = []
    for item in data.items():
      if (float(item[1]) > 0):
        hist_data.append(float(item[1]))
    data = sorted(data.items(), key=lambda kv:kv[1])
    for item in data: print(item)
    bins = np.arange(min(hist_data), max(hist_data), 0.01)
    ax1 = plt.subplot(211)
    plt.title('8-year Geometric Return on Investment Capital')
    plt.xlim([0, max(hist_data)])
    ax1.hist(hist_data, bins=bins, normed=True, alpha=0.8)
    shape, loc, scale = lognorm.fit(hist_data)
    pdf = lognorm.pdf(bins,shape,loc,scale)
    ax1.plot(bins,pdf,'r')
    ax2 = plt.subplot(212)
    cdf = lognorm.cdf(bins,shape,loc,scale)
    ax2.plot(bins,cdf,'r')
    plt.show()
  if args.plotGPA:
    gatherer = gpa.GPAGatherer(args.plotGPA, os.environ[cache_varname])
    for data in gatherer.datadict.items():
      plt.plot(data[1])
    plt.ylabel("Growth to assets ratio")
    plt.show()
  if (args.histGPA==True):
    gatherer = gpa.GPAGatherer("all", os.environ[cache_varname])
    data = gatherer.mostrecent()
    hist_data = []
    for item in data.items():
      if (float(item[1]) > 0):
        hist_data.append(float(item[1]))
    data = sorted(data.items(), key=lambda kv:kv[1])
    for item in data: print(item)
    bins = np.arange(min(hist_data), max(hist_data), 0.05)
    ax1 = plt.subplot(211)
    plt.title('Growth to assets ratio')
    plt.xlim([min(hist_data), max(hist_data)])
    ax1.hist(hist_data, bins=bins, normed=True, alpha=0.8)
    shape, loc, scale = lognorm.fit(hist_data)
    pdf = lognorm.pdf(bins,shape,loc,scale)
    ax1.plot(bins,pdf,'r')
    ax2 = plt.subplot(212)
    cdf = lognorm.cdf(bins,shape,loc,scale)
    ax2.plot(bins,cdf,'r')
    plt.show() 





