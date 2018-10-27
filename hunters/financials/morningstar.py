
import os
import urllib
from urllib import urlretrieve
from urllib2 import urlopen
import urlparse
import time

wikipedia_snp500_html_url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
cache_varname = "GREENLIGHT_CACHE_PATH"
snp500_symbols_filename = "snp500_symbols.txt"
commonstocks_ratios_cachedir_name   = os.path.join("stocks","ratios")
commonstocks_income_cachedir_name   = os.path.join("stocks","income")
commonstocks_cashflow_cachedir_name = os.path.join("stocks","cashflow")
commonstocks_balance_cachedir_name  = os.path.join("stocks","balance")

msKRstub  = "http://financials.morningstar.com/ajax/exportKR2CSV.html?t="
msFinSeg1 = "http://financials.morningstar.com/ajax/ReportProcess4CSV.html?t="
msFinSeg2 = "&reportType="
msFinSeg3 = "&period=12&dataType=A&order=asc&columnYear=5&number=3"

def pull_financials(cache_path):
  cached_symbols_filepath = os.path.join(cache_path, snp500_symbols_filename)
  ratios_dir   = os.path.join(cache_path, commonstocks_ratios_cachedir_name)
  if not os.path.isdir(ratios_dir): os.mkdir(ratios_dir)
  income_dir   = os.path.join(cache_path, commonstocks_income_cachedir_name)
  if not os.path.isdir(income_dir): os.mkdir(income_dir)
  cashflow_dir = os.path.join(cache_path, commonstocks_cashflow_cachedir_name)
  if not os.path.isdir(cashflow_dir): os.mkdir(cashflow_dir)
  balance_dir  = os.path.join(cache_path, commonstocks_balance_cachedir_name)
  if not os.path.isdir(balance_dir): os.mkdir(balance_dir)
  puller = urllib.URLopener()
  with open(cached_symbols_filepath, 'r') as cached_symbols_file:
    for line in cached_symbols_file:
      symbol = line.strip("\n")
      print("Pulling financial data for " + symbol)
      msURL = msKRstub + symbol
      try:
        #os.system("curl -G " + msURL + " -q -o " + os.path.join(ratios_dir, symbol + ".txt"))
        puller.retrieve(msURL, os.path.join(ratios_dir, symbol + ".txt"))
        #Income Statement
        msURL = msFinSeg1 + symbol + msFinSeg2 + 'is' + msFinSeg3
        puller.retrieve(msURL, os.path.join(income_dir, symbol + ".txt"))
        #Cash Flow
        msURL = msFinSeg1 + symbol + msFinSeg2 + 'cf' + msFinSeg3
        puller.retrieve(msURL, os.path.join(cashflow_dir, symbol + ".txt"))
        #Balance sheed
        msURL = msFinSeg1 + symbol + msFinSeg2 + 'bs' + msFinSeg3
        puller.retrieve(msURL, os.path.join(balance_dir, symbol + ".txt"))
      except IOError: print("ERROR: " + symbol)

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
  pull_financials(cache_dir)
