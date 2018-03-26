#!/bin/bash

map(){
test $# -lt 1 && exit
inter=$1

python <(
cat << "EOF"
import sys
import json
import socket
import struct

f=open(sys.argv[1])
obj=json.load(f)
f.close()

def ip_str2int(ip):
  packedIP = socket.inet_aton(ip)
  return struct.unpack("!L", packedIP)[0]

def hit(i,o):
  if i < o[0]['ip_from']:
    return False
  if i > o[-1]['ip_from']:
    return i < o[-1]['ip_to']
  l=0;r=len(o)-1;
  while True:
    m=(l+r)/2
    #print l,m,r
    #print o[l]['ip_from'],o[m]['ip_from'],o[r]['ip_from']
    if o[m]['ip_from'] > i and o[m+1]['ip_from'] > i:
      #print 'left'
      r=m
    elif o[m]['ip_from'] < i and o[m+1]['ip_from'] < i:
      #print 'right'
      l=m+1
    else:
      #print 'middle'
      break
  return (o[m]['ip_to'] > i) or (o[m+1]['ip_from'] == i)

def map(i):
  for k,v in obj.items():
    #print "hit: " + str(i) + ", " + str(k)
    if v and hit(i,v):
      return k
  return '--'

while True:
  try:
    l=raw_input().strip()
  except:
    break
  if l[0]=='t':
    i=l.split()[4]
    i=ip_str2int(i)
    cc=map(i)
  if cc!='--':
      print l
EOF
) $inter
}
