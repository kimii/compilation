import urllib
import urllib2
import json

import utils

class RequestHandler():
  def __init__(self):
    config = utils.get_conf()

    manager_url = config["manager_url"]

    self.node_id = config["node"]["node_id"]
    self.node_key = config["node"]["node_key"]

    self.get_next_task_url = utils.url_join([manager_url, "get_next_task"])
    self.notify_task_state_url = utils.url_join([manager_url, "notify_task_state"])
    self.auth_node_url = utils.url_join([manager_url, "auth_node"])

  def get_next_task(self):
    params = {"node_id": self.node_id, "node_key": self.node_key}; 
    opener = urllib2.build_opener()
    post_data = urllib.urlencode(params).encode('utf-8')
    return opener.open(self.get_next_task_url, post_data).read()
  
  def notify_task_state(self, task, ntype, time_used=''):
    params = {"node_id": self.node_id, "node_key": self.node_key, "task": task, "ntype": ntype}
    if time_used:
      params["time_used"] = time_used

    opener = urllib2.build_opener()
    post_data = urllib.urlencode(params).encode('utf-8')
    return opener.open(self.notify_task_state_url, post_data).read()

  def auth_node(self):
    params = {"node_id": self.node_id, "node_key": self.node_key}; 
    opener = urllib2.build_opener()
    post_data = urllib.urlencode(params).encode('utf-8')
    return opener.open(self.auth_node_url, post_data).read()
