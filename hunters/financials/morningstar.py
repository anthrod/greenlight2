
import os
import urllib
from urllib import urlretrieve
from urllib2 import urlopen
import urlparse
import time
import argparse

wikipedia_snp500_html_url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
cache_varname = "GREENLIGHT_CACHE_PATH"
snp500_symbols_filename = "snp500_symbols.txt"
market_symbols_filenames = ["nasdaq.csv", "nyse.csv", "amex.csv"]
commonstocks_ratios_cachedir_name   = os.path.join("stocks","ratios")
commonstocks_income_cachedir_name   = os.path.join("stocks","income")
commonstocks_cashflow_cachedir_name = os.path.join("stocks","cashflow")
commonstocks_balance_cachedir_name  = os.path.join("stocks","balance")

msKRstub  = "http://financials.morningstar.com/ajax/exportKR2CSV.html?t="
msFinSeg1 = "http://financials.morningstar.com/ajax/ReportProcess4CSV.html?t="
msFinSeg2 = "&reportType="
msFinSeg3 = "&period=12&dataType=A&order=asc&columnYear=5&number=3"

def getfile(url, filepath):
  if os.path.exists(filepath):
    return
  puller = urllib.URLopener()
  delay  = 2
  for i in range(0,5):
    puller.retrieve(url, filepath)
    if os.stat(filepath).st_size>0:
      with open(filepath, 'r') as thefile:
        for line in thefile:
          if "sorry." in line:
            print("Warning: Invalid download. Removing file: " + str(filepath))
            os.remove(filepath)
            break
      return
    time.sleep(delay)
    delay = delay*2
  if not os.path.exists(filepath): 
    return
  if os.stat(filepath).st_size==0:
    print("Warning: Could not get financial data. Removing file: " + str(filepath))
    os.remove(filepath)

def snp_symbols(cache_path):
  cached_symbols_filepath = os.path.join(cache_path, snp500_symbols_filename)
  symbols = []
  with open(cached_symbols_filepath, 'r') as symbolsfile:
    for line in symbolsfile:
      symbols.append(line.strip("\n"))
  print("Found " + len(symbols) + " to fetch")
  return symbols

def fetchsymbols(cache_path, args):
  if args.snp:
    print("Fetching S&P symbols ONLY")
    return snp_symbols(cache_path)
  fetch_largecap = args.largecap
  fetch_midcap = args.midcap
  fetch_smallcap = args.smallcap
  fetch_microcap = args.microcap
  fetch_nanocap = args.nanocap
  symbols = []
  for symbol_filename in market_symbols_filenames:
    print("Reading symbols from " + symbol_filename)
    with open( os.path.join(cache_path, symbol_filename), 'r' ) as symbolsfile:
      for line in symbolsfile:
        line = line.replace("\"","").strip("\n").strip("\r").strip(",")
        entries = line.split(",")
        if "Symbol" in line or "Invesco" in line or "ProShares" in line or " Fund" in line or " ETF" in line\
          or len(entries)!=9 or entries[3]=="n/a": continue
        if float(entries[3]) > 10000000000 and fetch_largecap:
          symbols.append(entries[0]) 
        elif float(entries[3]) > 2000000000 and fetch_midcap:
          symbols.append(entries[0]) 
        elif float(entries[3]) > 300000000 and fetch_smallcap:
          symbols.append(entries[0]) 
        elif float(entries[3]) > 50000000 and fetch_microcap:
          symbols.append(entries[0]) 
        elif float(entries[3]) > 0 and fetch_nanocap:
          symbols.append(entries[0]) 
  print("Aggregated " + str(len(symbols)) + " symbols")
  return symbols

def pull_financials(cache_path, args):
  symbols = fetchsymbols(cache_path, args)
  ratios_dir   = os.path.join(cache_path, commonstocks_ratios_cachedir_name)
  if not os.path.isdir(ratios_dir): os.mkdir(ratios_dir)
  income_dir   = os.path.join(cache_path, commonstocks_income_cachedir_name)
  if not os.path.isdir(income_dir): os.mkdir(income_dir)
  cashflow_dir = os.path.join(cache_path, commonstocks_cashflow_cachedir_name)
  if not os.path.isdir(cashflow_dir): os.mkdir(cashflow_dir)
  balance_dir  = os.path.join(cache_path, commonstocks_balance_cachedir_name)
  if not os.path.isdir(balance_dir): os.mkdir(balance_dir)
  puller = urllib.URLopener()
  for symbol in symbols:
    print("Pulling financial data for " + symbol)
    try:
      #Ratios
      msURL = msKRstub + symbol
      filepath = os.path.join(ratios_dir, symbol+".txt")
      getfile(msURL,filepath)
      #Income Statement
      msURL = msFinSeg1 + symbol + msFinSeg2 + 'is' + msFinSeg3
      filepath = os.path.join(income_dir, symbol + ".txt")
      getfile(msURL,filepath)
      #Cash Flow
      msURL = msFinSeg1 + symbol + msFinSeg2 + 'cf' + msFinSeg3
      filepath = os.path.join(cashflow_dir, symbol + ".txt")
      getfile(msURL,filepath)
      #Balance sheet
      msURL = msFinSeg1 + symbol + msFinSeg2 + 'bs' + msFinSeg3
      filepath = os.path.join(balance_dir, symbol + ".txt")
      getfile(msURL,filepath)
    except IOError: print("ERROR: " + symbol)

def verify_cache():
  if not cache_varname in os.environ or not os.path.isdir(os.environ[cache_varname]):
    print("Error: This program saves data to the directory in the user's "\
          + cache_varname + " directory. Please define this variable and try again")
    quit()

if __name__ == '__main__':
  """If running this script standalone, fetch S&P500 symbols and write the symbol file to
  a file in the user's cache_varname directory"""
  parser = argparse.ArgumentParser(description="See numbers. Burn money.")
  parser.add_argument("--snp", "-u", dest="snp", default=False, action="store_true")
  parser.add_argument("--largecap", dest="largecap", default=False, action="store_true")
  parser.add_argument("--midcap", dest="midcap", default=False, action="store_true")
  parser.add_argument("--smallcap", dest="smallcap", default=False, action="store_true")
  parser.add_argument("--microcap", dest="microcap", default=False, action="store_true")
  parser.add_argument("--nanocap", dest="nanocap", default=False, action="store_true")
  args = parser.parse_args()
  verify_cache()
  cache_dir = os.environ[cache_varname] 
  pull_financials(cache_dir, args)
