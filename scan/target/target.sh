#!/bin/bash

get(){
cl=$( #country list
cat << "EOF"
TW
HK
IR
PK
SY
IQ
AF
LY
EOF
)

tl=$( #table list
cat << "EOF"
aiwen_data
ip2location_data
ip2locationlite_data
maxmind_data
EOF
)

mkdir -p .tmp/; cd .tmp/
for c in ${cl[@]}; do
  for t in ${tl[@]}; do
   echo "python country_query.py -c $c -t $t -o $c.$t"
   python ../country_query.py -c $c -t $t -o $c.$t
  done
done
cd ../
}

aggr(){
export LC_COLLATE=C #otherwise [A-Z] will not be case-sensitive

ls .tmp/[A-Z][A-Z].* | sort | xargs -I {} bash -c 'echo \#$(basename {}); cat {}; echo' | python <(
cat << "EOF"
import json
d={}
j=""
while True:
  try:
    l=raw_input().strip()
  except:
    break
  if not l:
    continue
  if l[0]=='#':
    if j:
      o=json.loads(j)
      if not d.has_key(f[0]):
        d[f[0]]={}
      d[f[0]][f[1]]=o
      j=""
    f=l.lstrip('#').split('.')
  else:
    j+=l
print json.dumps(d)
EOF
)
}

check(){
python <(
cat << "EOF"
import sys
import json
o=json.loads(sys.stdin.read())
for k,v in o.items():
  if type(v) == type({}):
    for vk,vv in v.items():
      print k + ": " + vk + ", " + str(len(vv))
  elif type(v) == type([]):
    print k + ": " + "intersect, " + str(len(v))
EOF
)
}

merge(){
test $# -lt 1 && exit
python <(
cat << "EOF"
import sys
import json

type=sys.argv[1]

d={}
o=json.loads(sys.stdin.read())
for k,v in o.items(): #k is country
  d[k]=[]
  l={}
  for vk in v.keys(): #vk is database
    v[vk].sort(key=lambda x:x["ip_from"])
    l[vk]=[0,0]
  m=[]
  while True: #merge
    cm=float('inf')
    p=""
    ck=""
    clear=True
    for vk in v.keys():
      if l[vk][0] >= len(v[vk]):
        continue
      clear=False
      f=v[vk][l[vk][0]]["ip_from"]
      t=v[vk][l[vk][0]]["ip_to"]
      if not l[vk][1] and f<cm:
        cm=f
        p='f'
        ck=vk
      elif t<cm:
        cm=t
        p='t'
        ck=vk
      
    if clear:
      break
    if p=='f':
      l[ck][1]=1
    else:
      l[ck][0]+=1
      l[ck][1]=0
    m.append([cm,p])

  cf=0
  ff=''
  for i in range(len(m)):
    if m[i][1]=='f':
      if cf==0:
        ff=m[i][0]
      cf+=1
    else:
      if type=="inter" and cf==len(v.keys()):
        d[k].append({"ip_from":m[i-1][0], "ip_to":m[i][0]})
      cf-=1
      if type=="union" and cf==0:
        d[k].append({"ip_from":ff, "ip_to":m[i][0]})
print json.dumps(d)
EOF
) $1
}

gen(){
g=$1
python <(
cat << "EOF"
import sys
import json
import socket
import struct

def ip_int2str(i):
  return socket.inet_ntoa(struct.pack('!L',i)) 

o=json.loads(sys.stdin.read())
g=int(sys.argv[1])
for k,v in o.items():
  for vv in v:
    for i in range(vv['ip_from'],vv['ip_to']+1,2**(32-g)):
      print ip_int2str(i)
EOF
) $g
}



##EXAMPLE
#get
#aggr > aggr
#cat aggr | merge inter > inter
#cat aggr | check
#cat inter | check

#cat inter | gen 28 >targets 



#MAIN
usage(){
echo 'target.sh <$command> [$options]'
echo 'COMMANDS:'
echo '  gen_target_from_geodb <-p $output_file_name_prefix> [-o sample_policy] [-d sample_density]'
echo '  gen_target_from_bgp'
}
test $# -lt 1 && usage && exit

OPTIND=2
while getopts "qp:t:f:" opt; do
  case "$opt" in
    q)
      quiet=1 ;;
    p)
      prefix=$OPTARG ;;
    o)
      policy=$OPTARG ;;
    d)
      density=$OPTARG ;;
    *)
      usage
      exit -1;;
  esac
done

cmd=$1
case $cmd in
  "gen_target_from_geodb")
    test -z "${prefix+x}" && usage && exit
    density=${density:=28}; policy=${policy:='union'}

    test ! -d .tmp && get

    test -z "${quiet+x}" && echo "aggr > $prefix.aggr" >&2
    aggr > $prefix.aggr

    test -z "${quiet+x}" && echo "cat $prefix.aggr | merge $policy > $prefix.$policy" >&2
    cat $prefix.aggr | merge $policy > $prefix.$policy

    test -z "${quiet+x}" && echo "cat $prefix.$policy | gen $density >$prefix.targets" >&2
    cat $prefix.$policy | gen $density >$prefix.targets 
    ;;
  *)
    usage
    exit;;
esac
