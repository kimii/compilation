import json
import time

from manager import http
from manager import utils

if __name__ == '__main__':
  config = utils.get_conf()
  HOST_NAME = config["host_name"]
  PORT_NUMBER = config["port_number"]
  httpd = http.Server( (HOST_NAME, PORT_NUMBER), http.Handler, config)
  print time.asctime(), "Server Starts - %s:%s" % (HOST_NAME, PORT_NUMBER)
  try:
    httpd.serve_forever()
  except KeyboardInterrupt:
    pass
  httpd.server_close()
  print time.asctime(), "Server Stops - %s:%s" % (HOST_NAME, PORT_NUMBER)
