#!/bin/bash
kill -9 $(pgrep -f run.p)
kill -9 ${pgrep -f main.py}
. env.sh TEST
dtach -n /tmp/monitormain.sock python backends/webui/main.py
ulimit -n 4096 && dtach -n /tmp/monitorrun.sock python backends/monitor/run.py
