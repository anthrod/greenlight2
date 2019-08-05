
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
commonstocks_10k_cachedir_name = os.path.join("stocks","10K")
edgar_cikmap_filename = "cik_ticker.csv"
edgar_addresses_dirname = "edgar-addresses"

cik_ticker_url = "http://rankandfiled.com/static/export/cik_ticker.csv"

edgar_url_stub = "https://www.sec.gov/Archives/"

quarter_edgar_tsv_identifiers = ["QTR1", "QTR2", "QTR3", "QTR4"]

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

def handleMissingEdgarIndex(edgar_addresses_dirpath):
  print("Downloading EDGAR address tables to \"" + edgar_addresses_dirpath + "\"")
  if not os.path.exists(edgar_addresses_dirpath): 
    os.mkdir(edgar_addresses_dirpath)
  import edgar
  edgar.download_index(edgar_addresses_dirpath, 1993) 

def download_10k(url, dest):
  with open(dest, "w+") as outputfile:
    with urllib.request.urlopen(url) as response:
      lines = response.read().decode('utf-8').split('\n')
      for line in lines:
        outputfile.write( line + "\n" )
  if os.stat(dest).st_size==0:
    raise IOError("Could not download from " + url)    

def pull_financials(cache_path, args):
  symbols = fetchsymbols(cache_path, args)
  data_dir   = os.path.join(cache_path, commonstocks_10k_cachedir_name)
  edgar_cikmap_filepath = os.path.join(os.environ[cache_varname], edgar_cikmap_filename)
  if os.path.exists(edgar_cikmap_filepath) and args.purgeOldData:
    os.remove(edgar_cikmap_filepath)
  if not os.path.exists(edgar_cikmap_filepath):
    print("Downloading CIK->symbol map file to \"" + edgar_cikmap_filepath + "\"")
    download_cik_ticker() 
  if os.path.isdir(data_dir) and args.purgeOldData: shutil.rmtree(data_dir)
  if not os.path.isdir(data_dir): os.mkdir(data_dir)
  edgar_addresses_dirpath = os.path.join(os.environ[cache_varname], edgar_addresses_dirname)
  if os.path.isdir(edgar_addresses_dirpath) and args.purgeOldData:
    shutil.rmtree(edgar_addresses_dirpath)
  if not os.path.isdir(edgar_addresses_dirpath):
    handleMissingEdgarIndex(edgar_addresses_dirpath)
  edgar_address_files = os.listdir(edgar_addresses_dirpath)
  if len(edgar_address_files)==0:
    handleMissingEdgarIndex(edgar_addresses_dirpath)    
  cikmap = fetch_ticker_cik_map()
  for symbol in symbols:
    if not symbol in cikmap:
      print("Warning: Could not find symbol \"" + symbol + "\" in the CIK->symbol map. Won't be able to fetch data")
      continue
    cik = cikmap[symbol]
    symbol_dir = os.path.join(data_dir, symbol)
    if not os.path.isdir(symbol_dir):
      os.mkdir(symbol_dir)
    print("Pulling 10-K reports for " + symbol)
    for addressfilename in edgar_address_files:
      year = addressfilename[0:4]
      address_filepath = os.path.join(edgar_addresses_dirpath, addressfilename)
      with open(address_filepath, "r") as addressfile:
        lines = addressfile.read().split("\n")
        for line in lines:
          if cik in line[0:7] and "|10-K|" in line:
            url = edgar_url_stub + line.split("|")[5]
            datafilename = os.path.join(os.environ[cache_varname], commonstocks_10k_cachedir_name)
            datafilename = os.path.join(datafilename, symbol)
            datafilename = os.path.join(datafilename, year + ".txt")
            #print(symbol + ", " + year + ", " + url + " =-> " + datafilename ) 
            if os.path.exists(datafilename):
              print(datafilename + " exists")
            else:
              print("Downloading " + datafilename + " from " + url)
              download_10k(url, datafilename)

def verify_cache():
  if not cache_varname in os.environ or not os.path.isdir(os.environ[cache_varname]):
    print("Error: This program saves data to the directory in the user's "\
          + cache_varname + " directory. Please define this variable and try again")
    sys.exit(1)

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
