import HTMLParser
import os
import sys
import json
import time

import multi_thread
import utils

#html parsers.
class CaidaParser(HTMLParser.HTMLParser):
  def __init__(self):
    HTMLParser.HTMLParser.__init__(self)
    self.img_cnt=0
    self.alt=""
    self.file=[]
    self.dir=[]

  def get_attr_value(self, target, attrs):
    for e in attrs:
      key = e[0]
      value = e[1]
      if (key == target):
        return value

  def handle_starttag(self, tag, attrs):
    if (tag == "img"):
      if (self.img_cnt >=2):
        alt_value = self.get_attr_value("alt", attrs)
        self.alt=alt_value
      self.img_cnt = self.img_cnt + 1
    
    if (tag == "a" and self.alt == "[DIR]"):
      href_value = self.get_attr_value("href", attrs)
      self.dir.append(href_value)
    elif (tag == "a" and self.alt != ""):
      href_value = self.get_attr_value("href", attrs)
      self.file.append(href_value)


#latest time.
#must be of the same length.
def time_cmp(t1, t2):
  for i in range(len(t1)):
    if (t1[i] != t2[i]):
      break
  if (i < len(t1)):
    return int(t1[i]) - int(t2[i])
  return 0

def get_latest_time_fromsite():
  opener = utils.get_caida_opener(utils.caida_trace_base_url)

  team_dir = ["team-1/daily/", "team-2/daily/", "team-3/daily/"]; 
  temp = []
  for t in team_dir:
    f = opener.open(utils.url_join([utils.caida_trace_base_url,t]))
    text = f.read()
    parser = CaidaParser()
    parser.feed(text)
    
    e = parser.dir[-1]
    temp.append(get_latest_date_from_year_dir(utils.url_join([utils.caida_trace_base_url,t,e]), opener))
  
  res = temp[0]
  for t in temp[1:]:
    if(time_cmp(t, res) > 0):
      res = t
  
  return res

def get_latest_date_from_year_dir(url, opener):
  f = opener.open(url)
  text = f.read()
  
  parser = CaidaParser()
  parser.feed(text)
  
  res = parser.dir[-1]
  res = res.split('-')[1].strip('/')
  return res

#file list from date
def get_url_list_from_date(date):
  opener = utils.get_caida_opener(utils.caida_trace_base_url)

  team_dir = ["team-1/daily/", "team-2/daily/", "team-3/daily/"]
  res = []
  for t in team_dir:
    f = opener.open(utils.url_join([utils.caida_trace_base_url,t]))
    text = f.read()
    parser = CaidaParser()
    parser.feed(text)
    
    target_year = date[:4]
  
    for e in parser.dir:
      if(time_cmp(e.strip('/'), target_year) == 0):
        res.extend( get_url_list_from_year_dir(date, utils.url_join([utils.caida_trace_base_url,t,e]), opener) )
        break
  
  return res

def get_url_list_from_year_dir(date, url, opener):
  f = opener.open(url)
  text = f.read()
  
  parser = CaidaParser()
  parser.feed(text)

  for e in parser.dir:
    d = e.split('-')[1].strip('/')
    if (time_cmp(d, date) == 0):
      return get_url_list_from_date_dir(utils.url_join([url,e]), opener)
  
  return []

def get_url_list_from_date_dir(url, opener):
  f = opener.open(url)
  text = f.read()
  
  parser = CaidaParser()
  parser.feed(text)

  res = []
  for e in parser.file:
    if ( len(e.split('.')) != 8 ):
      continue
    res.append(url+e)
  
  return res

#multi-thread wrapper for caida.
def download_caida_restricted_wrapper(argv, resources):
  url = argv[0]
  file_path = argv[1]
  
  #resource = resource[0]
  return download_caida_restricted_worker(url, file_path)

def download_caida_restricted_worker(url, file_path, resource=""):
  opener = utils.get_caida_opener(utils.caida_trace_base_url)

  if not os.path.exists(file_path):
    utils.touch(file_path)

  res = True
  ex = ''
  try:
    utils.log("downloading: " + url)
    if os.path.exists(file_path):
      f = opener.open(url, timeout=10)
      fp = open(file_path, 'wb')
      fp.write(f.read())
      fp.close();f.close()
  except Exception, e:
    utils.log(str(e))
    res = False
    ex = e
    if os.path.exists(file_path):
      os.remove(file_path)
  
  if res:
    utils.log( str(url.split('/')[-1]) + ' ' + str(res) + str(ex))
  
  return res

def get_caida_filename_from_url(url):
  team = url.split('/')[5]
  suffix = url.split('/')[-1].split('.',4)[-1]
  return team+"."+suffix

def download_date(date, directory, mt_num=-1):
  #get url list.
  is_succeeded = False
  round_cnt = 1
  while(not is_succeeded):
    try:
      url_list = get_url_list_from_date(date)
      is_succeeded = True
    except Exception, e:
      utils.log(str(e))
      is_succeed = False
      round_cnt = round_cnt + 1
      time.sleep(1*round_cnt)

  utils.touch(directory+'/')
  
  #resource list
  resources = ['']
  
  #build argv_list
  argv = []
  for url in url_list:
    file_path = utils.url_join([directory, get_caida_filename_from_url(url)])
    arg = (url, file_path)
    argv.append(arg)
  
  #run with multi thread.
  multi_thread.run_with_multi_thread(download_caida_restricted_wrapper, argv, resources, mt_num)
