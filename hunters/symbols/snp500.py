
import os

wikipedia_snp500_html_url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
snp500_symbols_filename = "snp500_symbols.txt"
cache_varname = "GREENLIGHT_CACHE_PATH"

def fetch_from_wikipedia():
  """Read SNP500 symbols from wikipedia.
  Returns a list of stock symbols for each stock
  on the S&P500 by reading wikipedia's S&P500 html page.
  """
  symbols = []
  #Get wikipedia page: curl -G <wikipedia_url> -o <temporary_filename>
  #Parse page to extract symbols list
  #Delete temporary_file
  return symbols

def fetch_snp500_symbols():
  """Return a list of symbols for each stock on the S&P500"""
  return fetch_from_wikipedia()

def write_symbols_to_file(filepath=snp500_symbols_filename):
  """Write all S&P500 symbols to file at filepath.
  One symbol per line in the file."""
  symbols = fetch_snp500_symbols()
  if len(symbols)==0:
    print("Error: Did not fetch any symbols")
    quit()
  #Write symbols to file here
  print("Wrote " + len(symbols) + " to " + filepath)

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
  cache_file = os.path.join(cache_dir,snp500_symbols_filename)
  write_symbols_to_file( cache_file )
