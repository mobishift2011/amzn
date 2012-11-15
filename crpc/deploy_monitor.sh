#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
export PYTHONPATH=$DIR:$PYTHONPATH
export ENV="TEST"
source /usr/local/bin/virtualenvwrapper.sh
workon crpc
kill -9 $(pgrep -f run.p)
kill -9 $(pgrep -f main.py)
rm /tmp/monitormain.sock /tmp/monitorrun.sock
dtach -n /tmp/monitormain.sock python backends/webui/main.py
ulimit -n 4096 && dtach -n /tmp/monitorrun.sock python backends/monitor/run.py
