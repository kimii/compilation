#
# collapse.sh -- collapse IP-level links to router-level links from aliases file and links file
# =============================================================================
# USAGE: see Usage below (./collapse.sh)
# INPUT: aliases file where each line is an alias pair
#        IP-level links file (see trace2link.pl)
# OUTPUT: same as the IP-level links file
#         1.in 2.out 3.is_dest 4.star 5.delay 6.freq 7.ttl 8.monitor
#         1. the IP address representing the ingress router, e.g., 1.2.3.4
#         2. the IP address representing the outgress router, e.g., 5.6.7.8
#         3. whether the outgress node is the destination, e.g., Y or N
#         4. the number of anonymous (*) hops inbetween, e.g., 0 for directed link
#         5. the minimal delay in ms > 0, e.g., 10
#         6. the cumulative frequence of link observed, e.g., 5000
#         7. the minimal TTL of the ingress interface, e.g., 7
#         8. the monoitor which observed the link at the minimal TTL, e.g., 9.0.1.2 
#
# CHANGE LOG:
# - 2018.3.09 - Alpha
#

#SUB
union(){
python <(
cat << "EOF"
#sub
def find(x):
  if not sets.has_key(x):
    sets[x] = [x,0]
    return x
  
  if sets[x][0] == x:
    return x
  else:
    return find(sets[x][0])

def union(x,y):
  rx = find(x)
  ry = find(y)
  if rx == ry:
    return
  if sets[rx][1] < sets[ry][1]:
    sets[rx][0] = ry
  elif sets[rx][1] > sets[ry][1]:
    sets[ry][0] = rx
  else:
    sets[ry][0] = rx
    sets[rx][1] += 1

#main
sets={}
while True:
  try:
    line=raw_input().strip()
  except:
    break
  f=line.split()
  union(f[0],f[1])

#out
d={}
for k in sets.keys():
  r=find(k)
  if not d.has_key(r):
    d[r] = [k]
  else:
    d[r].append(k)
for v in d.values():
  print ' '.join(sorted(v))
EOF
)
}

sub(){
python <(
cat << "EOF"
d={}

def find(x):
  if d.has_key(x):
    return d[x]
  return x

while True:
  line=raw_input().strip()
  if line=="#":
    break
  f=line.split()
  for i in f:
    d[i] = f[0]

while True:
  try:
    line=raw_input().strip()
  except:
    break
  f=line.split()
  print find(f[0]),find(f[1]),' '.join(f[2:])
EOF
) | sort -k 1,2 --parallel 4
}

merge(){
python <(
cat << "EOF"
#0.in 1.out 2.is_dest 3.star 4.delay 5.freq 6.ttl 7.monitor
def merge_attrs(al,bl):
  if bl[0] == 'N':
    al[0] = 'N'
  if int(bl[1]) < int(al[1]):
    al[1] = bl[1]
  if float(bl[2]) < float(al[2]):
    al[2] = bl[2]
  al[3] = str( int(al[3])+int(bl[3]) )
  if int(bl[4]) < int(al[4]) or (bl[4] == al[4] and bl[5] < al[5]):
    al[4:6] = bl[4:6]
  return al

p=[]
while True:
  try:
    line=raw_input().strip()
  except:
    print ' '.join(p)
    break
  if not line:
    continue

  f=line.split()
  if f[:2] != p[:2]:
    if p:
      print ' '.join(p)
    p = f
  else:
    p[2:] = merge_attrs(p[2:],f[2:])
  p=f
EOF
)
}

#MAIN
test $# -lt 2 && echo 'collapse $aliases $links' && exit

aliases=$1
links=$2
prefix=$(echo $links | sed 's/\.links$//')

cat <(cat $aliases | union | tee $prefix.rtrnodes) <(echo '#') $links | sub | merge
