
import os
import urllib2
import pytz
import pandas as pd
from datetime import datetime
from pandas.io.data import DataReader
import urllib
from urllib import urlretrieve
from urllib2 import urlopen

nasdaq_csv_url = "https://www.nasdaq.com/screening/companies-by-industry.aspx?exchange=NASDAQ&render=download"
nyse_csv_url = "https://www.nasdaq.com/screening/companies-by-industry.aspx?exchange=NYSE&render=download"
amex_csv_url = "https://www.nasdaq.com/screening/companies-by-industry.aspx?exchange=AMEX&render=download"

cache_varname = "GREENLIGHT_CACHE_PATH"

def getfile(url, filepath):
  puller = urllib.URLopener()
  delay  = 2
  for i in range(0,6):
    puller.retrieve(url, filepath)
    if os.stat(filepath).st_size>0:
      return
    time.sleep(delay)
    delay = delay*2

def getsymbols(cache_dir):
  nasdaqfilepath = os.path.join(cache_dir, "nasdaq.csv")
  print("Pulling NASDAQ symbol data...")
  getfile(nasdaq_csv_url, nasdaqfilepath) 
  nysefilepath = os.path.join(cache_dir, "nyse.csv")
  print("Pulling NYSE symbol data...")
  getfile(nyse_csv_url, nysefilepath) 
  amexfilepath = os.path.join(cache_dir, "amex.csv")
  print("Pulling AMEX symbol data...")
  getfile(amex_csv_url, amexfilepath) 

def verify_cache():
  if not cache_varname in os.environ or not os.path.isdir(os.environ[cache_varname]):
    print("Error: This program saves data to the directory in the user's "\
          + cache_varname + " directory. Please define this variable and try again")
    quit()

if __name__ == '__main__':
  """If running this script standalone, fetch S&P500 symbols and write the symbol file to
  a file in the user's cache_varname directory"""
  verify_cache()
  cache_dir = os.environ[cache_varname] 
  getsymbols(cache_dir)


