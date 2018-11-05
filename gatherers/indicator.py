
import sys
import os

class IndicatorGatherer(object):
  def __init__(self, symbol, cache_dir):
    self.symbol     = symbol
    self.cachedir   = cache_dir
    self.datadict   = {}
    if symbol=="all":
      self.getallentries()
    else:
      self.datadict[symbol] = self.fetchentry(symbol)
    self.postprocessdata()

  def getallentries(self):
    datadir = self.datadir()
    all_files = os.listdir(datadir)
    maxdatasize = 0
    for currentfile in all_files:
      symbol = currentfile.strip(".txt")
      data = self.fetchentry(symbol) 
      if len(data)>0 and not '' in data:
        data = [float(x) for x in data]
        maxdatasize = max(len(data),maxdatasize)
        self.datadict[symbol] = data
    for i in self.datadict.items():
      missing_data  = [0]*(maxdatasize - len(i[1]))
      missing_data += i[1]
      self.datadict[i[0]] = missing_data

  def postprocessdata(self):
    for item in self.datadict.items():
      currentsymbol = item[0]
      symboldata    = item[1]
      if '' in symboldata:
        print("Found blank entry in data: " + str(symboldata) + ", Replacing with mean")
        nums = [float(x) for x in symboldata if x!='']
        if sum(nums) == 0:
          print("Error: No valid quantities found in data for symbol " + self.symbol)
          del self.datadict[item[0]]
          continue
        nums_mean = sum(nums) / len(nums)
        for i in range(0,len(symboldata)):
          if symboldata[i]=='': symboldata[i] = nums_mean
        self.datadict[item[0]] = symboldata
      else:
        self.datadict[item[0]] = [float(x) for x in item[1]]

  def mostrecent(self):
    currentitems = {}
    for item in self.datadict.items():
      currentitems[item[0]] = item[1][-1]
    return currentitems
