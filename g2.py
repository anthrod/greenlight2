
import os
from datetime import datetime

from hunters.symbols import snp500
from hunters.timeseries import stocks

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
  timestamp_file_path = os.path.join(os.environ[cache_varname], timestamp_file_name)
  timenow = datetime.today()
  needs_update = False
  if not os.path.exists(timestamp_file_path):
    print("Could not find timestamp file \"" + timestamp_file_path + "\"")
  else:
    print("Reading timestamp file " + timestamp_file_path)
    cachetime = datetime(1970,1,1)
    with open(timestamp_file_path, 'r') as timestamp_file:
      for line in timestamp_file:
        if "Year:" in line:  cachetime = datetime(int(line.strip("Year: ")), cachetime.month, cachetime.day)
        if "Month:" in line: cachetime = datetime(cachetime.year, int(line.strip("Month: ")), cachetime.day)
        if "Day:" in line:   cachetime = datetime(cachetime.year, cachetime.month, int(line.strip("Day: "))) 
      time_since_last = timenow-cachetime
      if time_since_last.days < 1:
        print("Cache is up to date.")
        return
    timestamp_file.close()
  print("Updating S&P500 symbols...")
  snp500.update_snp500_symbols( os.environ[cache_varname] )  
  print("Pulling S&P500 time series data...")
  if not os.path.exists(os.path.join(os.environ[cache_varname], "stocks")):
    os.mkdir (os.path.join(os.environ[cache_varname], "stocks"))
  stocks.fetch_timeseries() 
  timestamp_file = open(timestamp_file_path, 'w')
  timestamp_file.write("Year: " + str(datetime.today().year) + "\n")
  timestamp_file.write("Month: " + str(datetime.today().month) + "\n")
  timestamp_file.write("Day: " + str(datetime.today().day) + "\n")
  timestamp_file.close() 
  

if __name__ == '__main__':
  checkCachePath()
  doUpdates()
