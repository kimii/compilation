import os
import sys
import time

import utils

#states = {'finished', 'unassigned', 'pending', 'terminated'}
#state database.
def init_state_file(start_time, end_time, file_path):
  utils.touch(file_path)
  fp = open(file_path, 'wb')
  write_state_lines(start_time, end_time, fp)

def update_state_file(end_time, file_path):
  utils.touch(file_path)

  fp = open(file_path,'r')
  last_day = fp.readlines()[-1].split()[0]
  start_time = utils.next_day(last_day)
  fp.close()

  fp = open(file_path,'a')
  write_state_lines(start_time, end_time, fp)
  
def write_state_lines(start_time, end_time, fp):
  y = int(start_time[:4])
  m = int(start_time[4:6])
  d = int(start_time[6:8])

  ey = int(end_time[:4])
  em = int(end_time[4:6])
  ed = int(end_time[6:8])
  
  while ( y < ey ):
    while ( m <= 12 ):
      num = utils.days_in_month(y, m)
      while( d <= num ):
        str = "%d%02d%02d" % (y, m, d)
        fp.write(str+" unassigned"+'\n')
        d = d + 1
      d = 1
      m = m + 1
    m = 1
    y = y + 1
  
  while ( m < em ):
    num = utils.days_in_month(ey, m)
    while ( d <= num ):
      str = "%d%02d%02d" % (y, m, d)
      fp.write(str+" unassigned"+'\n')
      d = d + 1
    d = 1
    m = m + 1
  
  while ( d <= ed ):
    str = "%d%02d%02d" % (y, m, d)
    fp.write(str+" unassigned"+'\n')
    d = d + 1

  fp.close()

def update_state(task_id, state, file_path):
  if not os.path.exists(file_path):
    utils.log("no such file: "+file_path)
    return

  fp = open(file_path, 'r')
  lines = fp.readlines()
  fp.close()

  fp = open(file_path, 'w')
  for line in lines:
    if (line.split()[0] == task_id):
      fp.write(task_id+" "+state+'\n')
    else:
      fp.write(line)
  fp.close()

def get_next_task(file_path):
  if not os.path.exists(file_path):
    utils.log("no such file: " + file_path)
    return

  fp = open(file_path, 'r')
  lines = fp.readlines()
  fp.close()

  for i in range(len(lines)-1, -1, -1):
    line = lines[i].strip()
    state = line.split()[1]
    if(state != "finished" and state != "pending" and state != "deleted"):
      return line.split()[0]


#authentication
def auth_node(node_id, node_key):
  conf = utils.get_conf()
  secret_file_path = conf['secret_file_path']
  if not os.path.exists(secret_file_path):
    utils.log('no such file: ' + secret_file_path)
    return False
  fp = open(secret_file_path, 'r')
  for line in fp.readlines():
    f = line.strip().split()
    if (f[0] == node_id and f[1] == node_key):
      fp.close()
      return True
  
  fp.close()
  return False

def on_notify(params):
  conf = utils.get_conf()
  log_file_path = conf['log_file_path']
  state_file_path = conf['state_file_path']
  fp = open(log_file_path, 'a')
  strftime = time.strftime("%Y-%m-%d %H:%M:%S")

  ntype = params['ntype']
  if (ntype == "finished"):
    node_id = params["node_id"]
    task = params["task"]
    time_used = params["time_used"]

    update_state(task, "finished", state_file_path)
    fp.write( "%s %s %s finished, time used: %s(s)\n" % (strftime, node_id, task, time_used) )
  elif (ntype in ["pending", "terminated"]):
    node_id = params["node_id"]
    task = params["task"]

    update_state(task, ntype, state_file_path)
    fp.write( "%s %s %s %s\n" % (strftime, node_id, task, ntype) )
  else:
    return False

  fp.close()
  return True
