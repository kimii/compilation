#!/bin/bash

#LOG
log(){
echo $1 >&2;
}
export -f log

#SUB
warts2link(){
test $# -lt 1 && echo 'warts2link $prefix.warts[.tar.gz;.gz]' && exit

input_file_path=$1
prefix=$(echo $input_file_path | sed 's/\.gz//' | sed 's/\.tar//')

log $prefix #debug
echo $prefix

(test ! -z "$(echo $input_file_path | grep -E '\.tar\.gz$')" && tar zxf $input_file_path -O || gzip -cd $input_file_path) | (test ! -z "$(echo $input_file_path | grep -E 'warts')" && sc_warts2text || cat) | perl trace2link.pl -p $prefix -
#output_file_path: $prefix.links
}

link2iface(){
test $# -lt 1 && echo 'link2iface $prefix.links' && exit

input=$1
prefix=$(echo $input | sed 's/\.links$//')

cat $input | python <(
cat << "END"
out={}
while True:
  try:
    line=raw_input()
  except:
    break
  fields = line.split()
  print fields[0] # 'from' must be a router iface
  if not out.has_key(fields[1]):
    out[fields[1]] = fields[2]
  elif fields[2] == "N":
    out[fields[1]] = "N"
for k,v in out.items():
  if v == "N":
    print k
END
) | sort | uniq >$prefix.ifaces
#output_file_path: $prefix.ifaces
}

link_coll(){
test $# -lt 2 && echo 'collapse $aliases $prefix.links' && exit

aliases=$1
links=$2
prefix=$(echo $links | sed 's/\.links$//')

./collapse.sh $aliases $links >$prefix.rtrlinks
#output_file_path: $prefix.rtrlinks
}

##
#CAIDA
#(warts)-[warts2link]->(links)-[linkmerge]->(links)
#(links)-[link2iface]->(ifaces)
#(ifaces)-[prober-ar]->(aliases)
#(aliases+links)-[linkcoll]->(rtrlinks)
##
preprocess_directory(){
test $# -lt 2 && exit

d=$1
test $(ls $d/ | wc -l) -eq 0 && echo "$d is empty" && exit
P=$2 #controll xargs concurrency

#(warts)-[warts2link]->(links)
export -f warts2link #export warts2link for xargs to call.
ll=($(ls $d/*.warts.gz | head -n 4 | xargs -I {} -n 1 -P $P bash -c 'warts2link {}'))

#(links)-[linkmerge]->(links)
echo "merging ${#ll[*]} files" >&2
for l in ${ll[*]}; do
  echo $l.links
done | perl linkmerge.pl >$d/$(basename $d).merged.links
echo "$d/$(basename $d).merged.links" >&2
#remove link
for l in ${ll[*]}; do
  echo "rm $l.links" >&2
  rm $l.links
done
}



#EXAMPLES
##example#1
#preprocess_directory /data/new/caida/20170307/ 6
#link2iface /data/new/caida/20180307/20180307.merged.links
#../scanner/prober /data/new/caida/20170307/20170307.merged.ifaces
#link_coll /data/new/caida/20170307/20170307.merged.aliases /data/new/caida/20170307/20170307.merged.ifaces

##example#2
#warts2link /data/new/caida/20180307/team-1.20180307.anc-us.warts.gz
#warts2link /data/new/20170610-0936.HK.warts.tar.gz
#link2iface /data/new/20170610-0936.HK.warts.links

##expample#3
#tar zxf /data/new/20170610.22110.iffinder.out.tar.gz -O | awk '$6 == "D" {print $1" "$2}' >/data/new/20170610-0936.HK.warts.aliases
#link_coll /data/new/20170610-0936.HK.warts.aliases /data/new/20170610-0936.HK.warts.links



#MAIN
usage(){
echo 'run.sh <$command> [$args]'
echo 'COMMANDS:'
echo '  process_caida_date <$directory> [$parallel=4]'
echo '  process_vps_date <$warts_file_path> <$iffinder_file_path>'
}
test $# -lt 1 && usage && exit

cmd=$1
case $cmd in
  "process_caida_date")
    test $# -lt 2 && usage && exit
    directory=$2; parallel=${3:=6}
    prefix=$directory/$(basename $directory)

    preprocess_directory $directory $parallel
    #link2iface $prefix.merged.links
    #../scanner/prober $prefix.merged.ifaces
    #link_coll $prefix.merged.aliases $prefix.merged.links
    ;;
  "process_vps_date")
    test $# -lt 3 && usage && exit
    warts_file_path=$2; iffinder_file_path=$3; 
    prefix=$(echo $input_file_path | sed 's/\.gz//' | sed 's/\.tar//')

    warts2link $warts_file_path
    link2iface $prefix.links
    tar zxf $iffinder_file_path -O | awk '$6 == "D" {print $1" "$2}' >$prefix.aliases
    link_coll $prefix.aliases $prefix.links
    ;;
  "combine_vps_directory")
    test $# -lt 2 && usage && exit
    directory=$2;
    prefix=$directory/$(basename $directory)

    preprocess_directory $directory 1
    ;;
  *)
    usage
    exit;;
esac
