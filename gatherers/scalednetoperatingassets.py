
from indicator import IndicatorGatherer
import sys
import os

commonstocks_balance_cachedir_name   = os.path.join("stocks","balance")

class ScaledNetOperatingAssetsGatherer(IndicatorGatherer):

  def datadir(self):
    return os.path.join(self.cachedir, commonstocks_balance_cachedir_name)

  def fetchentry(self, symbol):
    file_path = os.path.join(self.datadir(), symbol + ".txt")
    if not os.path.exists(file_path):
      print("Could not open file: " + file_path)
      return []
    total_assets = []
    cash = []
    liability_and_equity = []
    with open(file_path, "r") as financials_file:
      for line in financials_file:
        if "Total assets" in line:
          total_assets = line.strip("Total assets,").strip("\n").split(",")
        elif "Cash and cash equivalents" in line:
          cash = line.strip("Cash and cash equivalents,").strip("\n").split(",")
        elif "Total liabilities and stockholders' equity" in line:
          liability_and_equity = line.strip("Total liabilities and stockholders' equity,").strip("\n").split(",")

    snoa = []

    if len(total_assets)==len(cash) and len(cash)==len(liability_and_equity):
      for i in range(0,len(total_assets)):
        if total_assets[i]=="": total_assets[i] = "0"
        if cash[i]=="": cash[i] = "0"
        if liability_and_equity[i]=="": liability_and_equity[i] = "0"
        operating_assets = float(total_assets[i]) - float(cash[i])
        operating_liabilities = float(total_assets[i])-float(liability_and_equity[i]) 
        if float(total_assets[i])==0:
          snoa.append(1.0)
        else:
          snoa.append( (operating_assets-operating_liabilities)/float(total_assets[i]) )
      return snoa
    
    print("Error: Could not retrieve Scaled Net Operating Assets for symbol " + symbol)
    return snoa
