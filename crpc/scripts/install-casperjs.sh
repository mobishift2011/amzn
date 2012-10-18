#!/bin/bash 
sudo apt-get install libfontconfig

# install phantomjs first
curl http://phantomjs.googlecode.com/files/phantomjs-1.7.0-linux-x86_64.tar.bz2 -o /tmp/phantomjs.tar.bz2
sudo mkdir -p /opt/
sudo tar xjf /tmp/phantomjs.tar.bz2 -C /opt/
sudo ln -sf /opt/phantomjs-1.7.0-linux-x86_64/bin/* /usr/local/bin/

# then install casperjs
sudo mkdir -p /opt/casperjs
sudo rm -rf /opt/casperjs
sudo git clone git://github.com/n1k0/casperjs.git /opt/casperjs
sudo ln -sf /opt/casperjs/bin/* /usr/local/bin/
