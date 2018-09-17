

alphavantage_api_key = VB7RUOUTCDQMC6HE
alphavantage_base_url = "https://www.alphavantage.co/query?"
cache_varname = "GREENLIGHT_CACHE_PATH"
americanstocks_cachedir_name = "americanstocks"

class TimeseriesQuery(object):
  def __init__(
    self,
    symbol,
    function="TIME_SERIES_DAILY",
    output_size="full",
    file_type="csv",
    api_key=alphavantage_api_key
  ):
    self.querystring  = alphavantage_base_url + "function=" + function
    self.querystring += "\&symbol=" + symbol
    self.querystring += "\&outputsize=" + output_size
    self.querystring += "\&apikey=" + api_key

  def run(self, output_directory):
   """Run querystring html query, and save response to a file 
   named <symbol>.csv in directory output_filepath""" 
   pass

def get_symbols_list(cached_symbols_filepath):
  symbols = []
  #Read symbols from file
  return symbols

def fetch_timeseries(cached_symbols_filepath, timeseries_directorypath):
  symbols = get_symbols_list(cached_symbols_filepath)
  for symbol in symbols:
    #If timeseries file exists for this symbol, open it
    #Check if timeseries is updated to current day
    #If timeseries is already up-to-date, continue
    #If not up to date or file doesnt exist, get the data
      query = TimeseriesQuery(symbol)
      query.run(timeseries_directorypath)

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
  verify_cache()
  cache_dir = os.environ[cache_varname] 
  cached_symbols_filepath = os.path.join(cache_dir,snp500_symbols_filename)
  verify_symbols_file(cached_symbols_filepath)
  timeseries_directorypath = os.path.join(cache_dir,americanstocks_cachedir_name)
  if not os.path.exists(timeseries_directorypath): os.mkdir(timeseries_directorypath)
  fetch_timeseries(cached_symbols_filepath, timeseries_directorypath)
   
