import os
import sys
import json

#time utils.
def is_heap_year(year):
  if (not year % 400 or not year % 4):
    return True
  return False

def days_in_month(year, month):
  m2d = [0,31,28,31,30,31,30,31,31,30,31,30,31]

  return m2d[month]+(1 if month == 2 and is_heap_year(year) else 0)

def next_day(date):
  y=int(date[:4])
  m=int(date[4:6])
  d=int(date[6:8])
  
  num = days_in_month(y,m)
  if (d+1 > num):
    m = m + 1
    d = 1
    if (m > 12):
      y = y + 1
      m = 1
  else:
    d = d + 1
  
  str = "%d%02d%02d" % (y, m, d)
  return str

#path utils
def path_join(ul):
  s = []
  for u in ul:
    s += filter( lambda x:x, u.split('/') )
  return ('/' if ul[0][0]=='/' else '') + '/'.join(s) + ('/' if ul[-1][-1]=='/' else '')

def touch(file_path):
  file_path = path_join([file_path])
  f = file_path.rsplit('/',1)
  if len(f) == 1:
    open(file_path,'wb').close()
  else:
    if f[0] and not os.path.exists(f[0]):
      os.makedirs(f[0])
    if f[1] and not os.path.exists(file_path):
      open(file_path,'wb').close()

#log
def log(string):
    sys.stderr.write(string + '\n')
    sys.stderr.flush()

#config.
def get_conf():
  if not os.path.exists('config.json'):
    log('no such file: config.json\n') 
    exit()

  fp = open('config.json')
  conf = json.load(fp)['manager']
  fp.close()
  
  return conf
