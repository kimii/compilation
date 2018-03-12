import sys
import time
import json

from worker import caida, iplane, ripe_atlas
from worker import request_handler
from worker import utils

def download_date(download_type, task, directory, mt_num):
  if download_type == "caida":
    caida.download_date(task, directory, mt_num=mt_num)
  elif download_type == "iplane":
    file_path = utils.path_join([directory, task+'.tar.gz'])
    iplane.donwload_date(task, file_path, mt_num=mt_num)
  elif download_type == "ripe_atlas":
    file_path = utils.path_join([directory, task+'.gzip'])
    ripe_atlas.donwload_date(task, file_path, mt_num=mt_num)

def main(argv):
  conf = utils.get_conf()
  download_type = conf["download_type"]
  download_dir = conf["download_dir"]
  handler = request_handler.RequestHandler()
  
  if download_type in ["caida","iplane","ripe_atlas"]:
    while(True):
      try:
        res = json.loads(handler.get_next_task())
        if res["status"]:
          utils.log('>> failed to get next task: ' +res['message'])
          exit()
        task = res['data']
        
        start_time = time.time()
        res = json.loads(handler.notify_task_state(task, 'pending'))
        if res["status"]:
          utils.log('>> failed to notify manager: ' +res['message'])
          exit()
        utils.log('<< start downloading: ' + task)
        download_date(download_type, task, utils.path_join([download_dir,task]), mt_num=4)
    
        end_time = time.time()
        time_used = end_time - start_time
        utils.log('<< finsihed downloading: ' + task)

        res = json.loads(handler.notify_task_state(task, 'finished', time_used))
        if res["status"]:
          utils.log('>> failed to notify manager: ' +res['message'])
          exit()
        
      except KeyboardInterrupt:
        res = json.loads(handler.notify_task_state(task, 'terminated'))
        utils.log('<< terminated the download of: ' + task)
        if res["status"]:
          utils.log('>> failed to notify manager: ' +res['message'])
          exit()
        break

if __name__ == "__main__":
  main(sys.argv)
