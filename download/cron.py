import os
import sys
import json
import time
from datetime import datetime, timedelta

from manager import manager
from manager import utils
from worker import caida, iplane, ripe_atlas

def check():
  config = utils.get_conf()
  download_type = config["download_type"]
  state_file_path = config["state_file_path"]
  start_time = config["init_start_time"]

  utils.log(">> getting latest time from: " + download_type)
  if download_type == "caida":
    end_time = caida.get_latest_time_fromsite()
  elif download_type == "iplane":
    end_time = iplane.get_latest_time_fromsite()
  elif download_type == "ripe_atlas":
    end_time = (datetime.now()-timedelta(days=2)).strftime("%Y%m%d")
  else:
    utils.log("invalide download type: " + download_type)
    exit()
  utils.log("<< end_time: " + end_time)

  if not os.path.exists(state_file_path):
    utils.log("<< init state file, start time: " + start_time)
    manager.init_state_file(start_time, end_time, state_file_path)
  else:
    utils.log("<< update state file")
    manager.update_state_file(end_time, state_file_path)

def main():
  while True:
    try:
      check()
      time.sleep(24*60*60)
    except Exception, e:
      utils.log(str(e))
      exit()

if __name__ == "__main__":
  main()
