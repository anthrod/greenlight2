
import margingrowth
import marginstability
import sys
import os

commonstocks_ratios_cachedir_name   = os.path.join("stocks","ratios")

class MaxMarginGatherer(object):
  def getData(self, cache_path):
    gm_gatherer = margingrowth.MarginGrowthGatherer("all", cache_path)
    gm_data = gm_gatherer.mostrecent()
    for item in gm_data.items():
      if (float(item[1]) > 0):
        gm_data[item[0]] = float(item[1])
    gm_data = sorted(gm_data.items(), key=lambda kv:kv[1])
    index = 1.0
    gm_data_dict = {}
    for item in gm_data:
      print(str(item[0]))
      gm_data_dict[item[0]] = index/len(gm_data) 
      index  += 1.0    

    ms_gatherer = marginstability.MarginStabilityGatherer("all", cache_path)
    ms_data = ms_gatherer.mostrecent()
    for item in ms_data.items():
      if (float(item[1]) > 0):
        ms_data[item[0]] = float(item[1])
    ms_data = sorted(ms_data.items(), key=lambda kv:kv[1])
    index = 1.0
    ms_data_dict = {}
    for item in ms_data:
      print(str(item[0]))
      ms_data_dict[item[0]] = index/len(ms_data) 
      index  += 1.0    

    mm_dict = {}
    for item in ms_data_dict.items():
      mm_dict[item[0]] = max(ms_data_dict[item[0]], gm_data_dict[item[0]])
    return mm_dict
