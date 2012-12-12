#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
export PYTHONPATH=$DIR:$PYTHONPATH
export ENV=$1
#export GEVENT_RESOLVER=ares
source /usr/local/bin/virtualenvwrapper.sh
workon crpc
