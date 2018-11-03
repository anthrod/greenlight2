
import matplotlib.pyplot as plt
import sys
import os

wikipedia_snp500_html_url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
cache_varname = "GREENLIGHT_CACHE_PATH"
commonstocks_ratios_cachedir_name   = os.path.join("stocks","ratios")

def plot_roc(symbol, cache_dir):
  ratios_dir = os.path.join(cache_dir, commonstocks_ratios_cachedir_name)
  file_path = os.path.join(ratios_dir, symbol + ".txt")
  if not os.path.exists(file_path):
    print("Could not open file: " + file_path)
    quit()
  EPS = []
  with open(file_path, "r") as financials_file:
    for line in financials_file:
      if "EPS %" in line:
        EPS = financials_file.next().strip("Year over Year,,").strip("\n").split(",")
  if len(EPS)==0:
    print("An error occured in reading Earnings Per Share")
    quit()
  plt.plot(EPS)
  plt.ylabel("Earnings Per Share")
  plt.show()
  

def verify_cache():
  if not cache_varname in os.environ or not os.path.isdir(os.environ[cache_varname]):
    print("Error: This program uses data in the user's "\
          + cache_varname + " directory. Please define this variable and try again")
    quit()

if __name__ == '__main__':
  """If running this script standalone, fetch S&P500 symbols and write the symbol file to
  a file in the user's cache_varname directory"""
  verify_cache()
  cache_dir = os.environ[cache_varname] 
  plot_roc(sys.argv[1], cache_dir)
