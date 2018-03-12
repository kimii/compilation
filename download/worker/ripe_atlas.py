import os
import sys
import json
import math
import time
import datetime
import subprocess
import urllib2

import multi_thread
import utils

#categorize by one-off
def download_ripe_atlas_detail_worker_wrapper(argv, resource):
  url=argv[0]
  temp_list=argv[1]
  ind=argv[2]
  text=download_ripe_atlas_detail_worker(url)
  if not text:
    return False
  
  utils.log( url + " True " + str(ind) )
  temp_list[ind] = text
  return True

def download_ripe_atlas_detail_worker(url):
  opener = urllib2.build_opener(urllib2.HTTPBasicAuthHandler())

  res = True
  ex = ''
  text = ""
  try:
    f = opener.open(url, timeout=10)
    text = f.read()
    f.close()
  except Exception, e:
    utils.log(str(e))
    res = False
    ex = e
  
  if not res:
    return ''

  return text

def download_ripe_atlas_list_wrapper(argv, resources):
  url=argv[0]
  temp_list=argv[1]
  ind=argv[2]
  page=download_ripe_atlas_list_worker(url)
  if not page:
    return False

  temp_list[ind] = page["results"]
  return True
  
def download_ripe_atlas_list_worker(url):
  opener = urllib2.build_opener(urllib2.HTTPBasicAuthHandler())

  res = True
  ex = ''
  text = ""
  try:
    f = opener.open(url, timeout=10)
    text=f.read()
    f.close()
  except Exception, e:
    utils.log(str(e))
    res = False
    ex = e
  
  if res:
    utils.log( url + str(res) + ' ' + str(ex) )
  else:
    return None
  
  return json.loads(text)

def get_measurements_list(start_ts, stop_ts, mt_num):
  page_size=500
  
  measurements_url = utils.url_join([utils.ripeatlas_base_url,"/measurements/"])
  params={}
  params["format"]="json"
  params["page_size"]=str(page_size)
  params["is_public"]="true"
  params["type"]="traceroute"
  params["af"]="4"
  params["start_time__gte"]=start_ts
  params["stop_time_lte"]=stop_ts

  #resource list.
  resources = [''] 

  result_list=[]
  #first page
  url=utils.construct_url(measurements_url, params)
  page=download_ripe_atlas_list_worker(url)
  page_num=int(math.ceil(float(page["count"])/page_size))
  result_list.extend( page["results"] )
  
  temp_list=[ "" for i in range(page_num+1) ]
  
  #build argv_list
  argv = []
  #for i in range(2,page_num+1):
  for i in range(2,3): #debug
    params["page"] = str(i)
    url = utils.construct_url(measurements_url, params)
    arg = (url, temp_list, i)
    argv.append(arg)
  
  #run with multi thread.
  multi_thread.run_with_multi_thread(download_ripe_atlas_list_wrapper, argv, resources, mt_num)

  for i in range(2, page_num+1):
    result_list.extend( temp_list[i] )

  return result_list

def download_date(date, file_path, mt_num=-1):
  start_ts=int(time.mktime(datetime.datetime.strptime(date, "%Y%m%d").timetuple()))
  stop_ts=start_ts+24*60*60+1

  #get url list.
  result_list = []

  is_succeeded = False
  round_cnt = 1
  while(not is_succeeded):
    try:
      result_list = get_measurements_list(start_ts, stop_ts, mt_num)
      is_succeeded = True
    except Exception, e:
      utils.log(str(e))
      is_succeed = False
      round_cnt = round_cnt + 1
      time.sleep(1*round_cnt)
  
  url_list=[]
  for r in result_list:
    url_list.append(r["result"])
  
  #temp_list to contain result content of url_list
  temp_list=[ "" for i in range(len(url_list)) ]

  #destination file_path.
  utils.touch(file_path)

  #resources.
  resources = ['']

  #build argv
  argv = []
  #for i in range(len(url_list)):
  for i in range(40): #debug
    url=url_list[i]
    arg = (url, temp_list, i)
    argv.append(arg)
  
  #run with multi thread.
  multi_thread.run_with_multi_thread(download_ripe_atlas_detail_worker_wrapper, argv, resources, mt_num)
  
  #output
  utils.log( "writting to file ... " )
  for i in range(len(result_list)):
    result_list[i]["results_json"]=temp_list[i]

  fp = open(file_path, 'wb')
  h = subprocess.Popen(['gzip', '-c', '-'], stdin=subprocess.PIPE, stdout=fp)
  #h.stdin.write(json.dumps(result_list,indent=1))
  for i in range(len(result_list)):
    h.stdin.write(json.dumps(result_list[i])+"\n")
  h.stdin.close(); fp.close()
