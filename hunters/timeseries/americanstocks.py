import os
import time

alphavantage_api_key = "VB7RUOUTCDQMC6HE"
alphavantage_base_url = "https://www.alphavantage.co/query?"
cache_varname = "GREENLIGHT_CACHE_PATH"
americanstocks_cachedir_name = "americanstocks"
snp500_symbols_filename = "snp500_symbols.txt"

class TimeseriesQuery(object):
  def __init__(
    self,
    symbol,
    output_directory,
    function="TIME_SERIES_DAILY",
    output_size="full",
    api_key=alphavantage_api_key
  ):
    self.querystring  = "curl -G " + alphavantage_base_url + "function=" + function
    self.querystring += "\&symbol=" + symbol
    self.querystring += "\&outputsize=" + output_size
    self.querystring += "\&datatype=csv"
    self.querystring += "\&apikey=" + api_key
    self.querystring += " -o " + os.path.join(output_directory,symbol) + ".csv"

  def run(self):
    #Limit is 5 per minute
    print("\nPatience...")
    time.sleep(13)
    print("Command: " + self.querystring)
    os.system(self.querystring) 

def get_symbols_list(cached_symbols_filepath):
  symbols = []
  #Read symbols from file
  with open(cached_symbols_filepath, 'r') as cached_symbols_file:
    for line in cached_symbols_file:
      symbols.append(line.strip("\n"))
  return symbols

def fetch_timeseries():
  verify_cache()
  cache_dir = os.environ[cache_varname] 
  cached_symbols_filepath = os.path.join(cache_dir,snp500_symbols_filename)
  verify_symbols_file(cached_symbols_filepath)
  timeseries_directorypath = os.path.join(cache_dir,americanstocks_cachedir_name)
  if not os.path.exists(timeseries_directorypath): os.mkdir(timeseries_directorypath)
  symbols = get_symbols_list(cached_symbols_filepath)
  for symbol in symbols:
    query = TimeseriesQuery(symbol, timeseries_directorypath)
    query.run()

def verify_cache():
  if not cache_varname in os.environ or not os.path.isdir(os.environ[cache_varname]):
    print("Error: This program saves data to the directory in the user's "\
          + cache_varname + " directory. Please define this variable and try again")
    quit()

def verify_symbols_file(symbols_filepath):
  if not os.path.exists(symbols_filepath):
    print("Could not find symbols file at " + symbols_filepath)
    print("Create this file and try again")
    quit()

if __name__ == '__main__':
  """If running this script standalone, fetch S&P500 symbols and write the symbol file to
  a file in the user's cache_varname directory"""
  fetch_timeseries()  
