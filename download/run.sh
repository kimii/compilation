usage(){
  echo "run manager/worker"
}
test $# -lt 1 && usage && exit

TYPE=$1

case $TYPE in
  "manager")
    tmux new-session \; \
      send-keys 'python cron.py 2>&1 | tee -a cron.log' C-m\; \
      split-window -v \; \
      send-keys 'python httpd.py 2>&1 | tee -a httpd.log' C-m\;
    ;;
  "worker")
    tmux new-session \; \
      send-keys 'python download.py 2>&1 | tee -a download.log' C-m\; \
    ;;
  *)
    usage
    exit;;
esac
