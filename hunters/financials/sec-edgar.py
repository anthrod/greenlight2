
import shutil
import os
import urllib
from urllib.request import urlretrieve
import time
import argparse

wikipedia_snp500_html_url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
cache_varname = "GREENLIGHT_CACHE_PATH"
snp500_symbols_filename = "snp500_symbols.txt"
market_symbols_filenames = ["nasdaq.csv", "nyse.csv", "amex.csv"]
commonstocks_10k_cachedir_name   = os.path.join("stocks","10K")
edgar_cikmap_filename = "cik_ticker.csv"

cik_ticker_url = "http://rankandfiled.com/static/export/cik_ticker.csv"

msKRstub  = "http://financials.morningstar.com/ajax/exportKR2CSV.html?t="
msFinSeg1 = "http://financials.morningstar.com/ajax/ReportProcess4CSV.html?t="
msFinSeg2 = "&reportType="
msFinSeg3 = "&period=12&dataType=A&order=asc&denominatorView=decimal&columnYear=5&number=3"

def getfile(url, filepath):
  if os.path.exists(filepath):
    return True
  puller = urllib.URLopener()
  delay  = 1
  print("Pulling from: " + url)
  for i in range(0,5):
    puller.retrieve(url, filepath)
    if os.stat(filepath).st_size>0:
      with open(filepath, 'r') as thefile:
        for line in thefile:
          if "sorry." in line:
            print("Warning: Invalid download. Removing file: " + str(filepath))
            os.remove(filepath)
            break
      return False
    time.sleep(delay)
    delay = delay*2
  if not os.path.exists(filepath): 
    return False
  if os.stat(filepath).st_size==0:
    print("Warning: Could not get financial data. Removing file: " + str(filepath))
    os.remove(filepath)
    return False
  return True

def download_cik_ticker(url=cik_ticker_url, filepath=os.path.join(os.environ[cache_varname], edgar_cikmap_filename)):
  with open(filepath, "w+") as outputfile:
    with urllib.request.urlopen(url) as response:
      lines = response.read().decode('utf-8').split('\n')
      print(lines)
      for line in lines:
        outputfile.write( line + "\n" )
  if os.stat(filepath).st_size==0:
    raise IOError("Could not download from " + url)    

def snp_symbols(cache_path):
  cached_symbols_filepath = os.path.join(cache_path, snp500_symbols_filename)
  symbols = []
  with open(cached_symbols_filepath, 'r') as symbolsfile:
    for line in symbolsfile:
      symbols.append(line.strip("\n"))
  print("Found " + str(len(symbols)) + " symbols to fetch")
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
        symbolname = entries[0]
        if float(entries[3]) > 10000000000 and fetch_largecap:
          symbols.append(symbolname) 
        elif float(entries[3]) > 2000000000 and fetch_midcap:
          symbols.append(symbolname) 
        elif float(entries[3]) > 300000000 and fetch_smallcap:
          symbols.append(symbolname) 
        elif float(entries[3]) > 50000000 and fetch_microcap:
          symbols.append(symbolname) 
        elif float(entries[3]) > 0 and fetch_nanocap:
          symbols.append(symbolname) 
  print("Aggregated " + str(len(symbols)) + " symbols")
  return symbols

def fetch_ticker_cik_map(filepath=os.path.join(os.environ[cache_varname], edgar_cikmap_filename)):
  cik_map = {}
  with open(filepath, "r") as cik_ticker_file:
    lines = cik_ticker_file.read().split('\n')
    lines = lines[1:]
    for line in lines:
      entries = line.split("|")
      if len(entries)<8: 
        continue
      cik_map[entries[1]] = entries[0]
  return cik_map

def pull_financials(cache_path, args):
  symbols = fetchsymbols(cache_path, args)
  cikmap = fetch_ticker_cik_map()
  data_dir   = os.path.join(cache_path, commonstocks_10k_cachedir_name)
  if os.path.isdir(data_dir) and args.purgeOldData: shutil.rmtree(data_dir)
  if not os.path.isdir(data_dir): os.mkdir(data_dir)
  for symbol in symbols:
    symbol_dir = os.path.join(data_dir, symbol)
    if not os.path.isdir(symbol_dir):
      os.mkdir(symbol_dir)
    print("Pulling financial data for " + symbol)
          

def verify_cache():
  if not cache_varname in os.environ or not os.path.isdir(os.environ[cache_varname]):
    print("Error: This program saves data to the directory in the user's "\
          + cache_varname + " directory. Please define this variable and try again")
    sys.exit(1)
  edgar_cikmap_filepath = os.path.join(os.environ[cache_varname], edgar_cikmap_filename)
  if not os.path.exists(edgar_cikmap_filepath):
    print("Warning: Could not find CIK->symbol map file at " + edgar_cikmap_filepath)
    print("Attempting to download...")
    download_cik_ticker() 

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
  parser.add_argument("--purge", dest="purgeOldData", help="Purge/delete any existing data first", action="store_true")
  args = parser.parse_args()
  verify_cache()
  cache_dir = os.environ[cache_varname] 
  pull_financials(cache_dir, args)
