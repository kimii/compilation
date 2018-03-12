import sys
import time
import json
import BaseHTTPServer
import cgi

import manager
import utils

ERR={
-1:"invalid action",
0:"success",
1:"failed",
2:"server error"
}

class Server(BaseHTTPServer.HTTPServer):
  def __init__(self, (HOST_NAME, PORT_NUMBER), handler, config):
    BaseHTTPServer.HTTPServer.__init__(self, (HOST_NAME, PORT_NUMBER), handler)
    self.config = config
  
class Handler(BaseHTTPServer.BaseHTTPRequestHandler):
  def do_HEAD(self):
    self.send_response(200)
    self.send_header("Content-type", "text/html")
    self.end_headers()
  def do_GET(self):
    self.send_response(200)
    self.send_header("Content-type", "text/html")
    self.end_headers()
  def do_POST(self):
    action = self.path.replace('/','')
    valid_action = [ "get_next_task", "notify_task_state", "auth_node" ]
    if ( action not in valid_action ):
      utils.log('invalide action: ' + action)
      output = {}
      output['status'] = -1
      output['message'] = ERR[-1]
      output['data'] = action
      self.wfile.write(json.dumps(output, indent=2))
      return
    
    post = cgi.FieldStorage(
      fp=self.rfile, 
      headers=self.headers,
      environ={'REQUEST_METHOD':'POST',
      'CONTENT_TYPE':self.headers['Content-Type'],}
    )

    state_file_path = self.server.config["state_file_path"]
    if ( action == "get_next_task" ):
      task = manager.get_next_task(state_file_path)
      if task:
        output = {}
        output['status'] = 0
        output['message'] = ERR[0]
        output['data'] = task
        self.wfile.write(json.dumps(output, indent=2))
    elif ( action == "notify_task_state" ):
      node_id = post["node_id"].value
      node_key = post["node_key"].value
      task = post["task"].value
      ntype = post["ntype"].value
      params = {
        "task": task,
        "ntype": ntype,
        "node_id": node_id,
        "node_key": node_key
      }
      if (post.has_key("time_used")):
        params["time_used"] = post["time_used"].value
      
      if manager.on_notify(params):
        output = {}
        output['status'] = 0
        output['message'] = ERR[0]
        output['data'] = ''
        self.wfile.write(json.dumps(output, indent=2))
      else:
        output = {}
        output['status'] = 1
        output['message'] = ERR[1]
        output['data'] = ''
        self.wfile.write(json.dumps(output, indent=2))
    elif ( action == "auth_node" ):
      node_id = post["node_id"].value
      node_key = post["node_key"].value
      if manager.auth_node(node_id, node_key):
        output = {}
        output['status'] = 0
        output['message'] = ERR[0]
        output['data'] = ''
        self.wfile.write(json.dumps(output, indent=2))
      else:
        output = {}
        output['status'] = 1
        output['message'] = ERR[1]
        output['data'] = ''
        self.wfile.write(json.dumps(output, indent=2))
