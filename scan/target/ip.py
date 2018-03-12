import socket
import struct

def ip_str2int(ip):
	packedIP = socket.inet_aton(ip)
	return struct.unpack("!L", packedIP)[0]

def ip_int2str(i):
	return socket.inet_ntoa(struct.pack('!L',i)) 

def subnet2ip(subnet,g):
	f=subnet.split('/')
	g=max(g,int(f[1]))
	net=ip_str2int(f[0])/(2**(32-int(f[1])))*(2**(32-int(f[1])))
	res=[]
	for i in range( 1, (2**(32-int(f[1])))-1, (2**(32-g)) ):
		res.append( ip_int2str(net+i) )
	if not res:
		res.append(f[0])
	return res

def process(target):
	res_list=[]
	for ip in target.split('\n'):
		if ip=="":
			continue
		elif re.findall('/',ip):
			res_list.extend(subnet2ip(ip,30))
		else:
			res_list.append(ip)
	res_str=""
	for r in res_list:
		res_str += r+"\n"
	return res_str
