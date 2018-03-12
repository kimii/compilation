import os
import sys
import threading
import time
import json
import urllib2
import urllib
import cookielib

#multi thread
class TaskThread(threading.Thread):
  def __init__(self, target, args):
    threading.Thread.__init__(self, target=target, args=args);
    self.start_time = time.time();
  
  def get_time_alive(self):
    end_time = time.time();
    return end_time - self.start_time;

def get_alive_thread_cnt(th_pool):
  cnt_alive = 0;
  for i in range(len(th_pool)):
    t = th_pool[i];
    #if (t.is_alive() and t.get_time_alive() >= 1):
    if (t.is_alive() ):
      cnt_alive = cnt_alive + 1;
  for th in th_pool:
    if (not th.is_alive()):
      th_pool.remove(th);
  
  return cnt_alive;

def task_wrapper(func, argv, resource, res_list, started_list, ind):
  started_list[ind] = True;
  res = func(argv, resource)
  res_list[ind] = res;
  started_list[ind] = False;
  
#each task dependently owns 1 argv, 
#all tasks share 1 same resource list.
#type of resource is <type_list>.
def run_with_multi_thread(func, argv_list, resource_list, mt_num=-1): #list of argv(s)
  if (mt_num <= 1):
    for argv in argv_list:
      func(argv,[""])
  elif (mt_num > 1): 
    #use flags to keep track of stage of each task.
    is_finished = [False for i in range(len(argv_list))]; 
    is_started = [False for i in range(len(argv_list))];

    cur_resource = 0
    while(True):
        task_list = [];
        th_pool = [];
        has_started = False;
        for i in range(len(argv_list)):
          if (not is_finished[i] and not is_started[i]):
            task_list.append(i);
          if (is_started[i]):
            has_started = True;
            
        if (len(task_list) == 0 and not has_started): #end condition.
          break;
        
        for i in range(len(task_list)):
          argv = argv_list[task_list[i]]
          ind = task_list[i]
          resource = resource_list[cur_resource]
          cur_resource += 1
          if (cur_resource >= len(resource_list)):
            cur_resource = 0
            time.sleep(1)

          th = TaskThread(target=task_wrapper, args=(func,argv,resource,is_finished,is_started,ind));
          th_pool.append(th);
          th.start();
          
          while(get_alive_thread_cnt(th_pool) >= mt_num):
            time.sleep(1); #periodically checking available slot.

#log
def log(string):
    sys.stderr.write(string + '\n')
    sys.stderr.flush()

#config.
def get_conf():
  if not os.path.exists('config.json'):
    log('no such file: config.json') 
    exit()

  fp = open('config.json')
  conf = json.load(fp)
  fp.close()
  
  return conf["worker"]

#auth
def load_auth(auth_file):
  if not os.path.exists(auth_file):
    log('no such file: '+auth_file)
    exit()
  return json.load( open(auth_file) )
    
#caida
caida_trace_base_url = "https://topo-data.caida.org/team-probing/list-7.allpref24/"
caida_itdk_base_url = "https://topo-data.caida.org/ITDK/"

def get_caida_opener(url):
  auth_info = load_auth("accounts.json")
  username = auth_info["caida"]["username"]
  password = auth_info["caida"]["password"]

  passwd_mgr = urllib2.HTTPPasswordMgrWithDefaultRealm()
  passwd_mgr.add_password("topo-data", url, username, password)

  return urllib2.build_opener(urllib2.HTTPBasicAuthHandler(passwd_mgr))

#ripeatlas
ripeatlas_base_url = "https://atlas.ripe.net/api/v2/"

#iplane
iplane_base_url = "https://data-store.ripe.net/datasets/iplane-traceroutes/"
def get_iplane_opener():
  iplane_login_url = "https://access.ripe.net/?originalUrl=https%3A%2F%2Fdata-store.ripe.net%2Fdatasets%2Fiplane-traceroutes%2F&service=datarepo"
  auth_info = load_auth("accounts.json")
  username = auth_info["iplane"]["username"]
  password = auth_info["iplane"]["password"]

  params = { "username": username, "password": password }; 
  cj = cookielib.CookieJar()
  opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
  post_data = urllib.urlencode(params).encode('utf-8')
  
  f = opener.open(iplane_login_url, post_data)
  f.close()
  
  return opener

def construct_url(base, params):
  url=base+"/?"
  for k in params.keys():
    url+="%s=%s&"%(k,params[k])
  
  return url.strip("&")

#url
def url_join(ul):
  s = []
  for u in ul:
    s += filter( lambda x:x, u.split('/') )
  if s[0][-1] == ':':
    s[0]+='/'
  return ('/' if ul[0][0]=='/' else '') + '/'.join(s) + ('/' if ul[-1][-1]=='/' else '')

#path utils
#path_join holds '/' in the front and rear
def path_join(ul):
  s = []
  for u in ul:
    s += filter( lambda x:x, u.split('/') )
  return ('/' if ul[0][0]=='/' else '') + '/'.join(s) + ('/' if ul[-1][-1]=='/' else '')

#advanced touch
#touch $file_path create new directory
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

def dir_name(file_path):
  file_path = path_join([file_path])
  f = file_path.rsplit('/',1)
  if len(f) == 1:
    return '.'
  return f[0]

def file_name(file_path):
  file_path = path_join([file_path])
  f = file_path.rsplit('/',1)
  if len(f) == 1:
    return file_path
  return f[1]
