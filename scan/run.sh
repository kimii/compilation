#! /bin/bash
usage(){
  echo "usage: nohup run.sh task.json > log/task-$(date +%Y%m%d-%H:%M:%S).log 2>&1 &"
}

test $# -lt 1 && usage && exit
task=$1
cat $task

monitors=$(cat task.json | tr '\n' ' ' | python <(
cat <<"EOF"
import json
t=json.loads(raw_input())
for m in t['task']['monitor']:
    print m
EOF
)
)

target=$(cat task.json | tr '\n' ' ' | python <(
cat <<"EOF"
import json
t=json.loads(raw_input())
if t['task']['target'].has_key('generate_target'):
  print t['task']['target']['generate_target']['data_dir']
elif t['task']['target'].has_key('specific_target'):
  print t['task']['target']['specific_target']['data_dir']
EOF
)
)

if [ ! -z "$(cat task.json | grep \"generate_target\")" ]; then
  #rm -r ./target/data/.tmp
  #mkdir -p .tmp/
  #./target/target.sh gen_target_from_geodb -p /home/cmn/compilation/scan/target/test/$(date +%Y%m%d-%H:%M:%S).targets
  for m in ${monitors[@]}; do
    echo "nohup ./manager run_trace $m $target > log/${m}-$(date +%Y%m%d-%H:%M:%S).log 2>&1 &"
    nohup ./manager run_trace $m $target > log/${m}-$(date +%Y%m%d-%H:%M:%S).log 2>&1 &
    sleep 30
  done
elif [ ! -z "$(cat task.json | grep \"specific_target\")" ]; then
  for m in ${monitors[@]}; do
    echo "nohup ./manager specific_target $m $target > log/${m}-$(date +%Y%m%d-%H:%M:%S).log 2>&1 &"
    nohup ./manager specific_target $m $target > log/${m}-$(date +%Y%m%d-%H:%M:%S).log 2>&1 &
  done
else
  echo "check wrong task.json"
fi
   

