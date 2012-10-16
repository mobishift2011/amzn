#!/bin/bash
sudo apt-get -y install build-essential python-dev libevent-dev libxslt-dev uuid-dev python-setuptools dtach libzmq-dev
sudo apt-get -y install sysstat vnstat redis-server mysql-server
sudo easy_install pip
sudo pip install virtualenvwrapper

source /usr/local/bin/virtualenvwrapper.sh
mkvirtualenv crpc
workon crpc
pip install --upgrade cython
pip install -r requirements.txt
