#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
export PYTHONPATH=$DIR:$PYTHONPATH
export ENV=TEST
source /usr/local/bin/virtualenvwrapper.sh
workon crpc
kill -9 $(pgrep -f run.p)
kill -9 $(pgrep -f main.py)
ulimit -n 4096 && nohup python backends/monitor/run.py &
cd backends/webui
nohup python main.py &
