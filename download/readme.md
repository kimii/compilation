# prerequisites:
 - tmux

# usage:
 - create secret file:

		# looks something like this
		node_001 password_for_node_001

 - config.json:

		# change the corresponding section,
	        # according to role
		{
		  "manager":{
		    "init_start_time":"20070101",
		    "download_type":"**<caida/iplane/ripeatlas>**",
		    "host_name":"**<public ip>**",
		    "port_number":**<port>**,
		    "state_file_path":"files/state",
		    "log_file_path":"files/log",
		    "secret_file_path":"**<secret_file_path>**"
		  },
		
		  "worker":{
		    "manager_url":"**http://<manager_ip>:<manager_port>**",
		    "download_type":"**<caida/iplane/ripeatlas>**",
		    "download_dir":"**<destination directory>**",
		    "node":{
		      "node_id":"**<node_id>**",
		      "node_key":"**<node_key>**"
		    }
		  }
		}
	
 - run:

 		./run.sh manager

		# or 

		./run.sh worker
