#!/bin/bash 
sudo apt-get install firefox chromium-browser
sudo apt-get install xvfb

sudo ln -s /usr/bin/chromium-browser /usr/bin/google-chrome

echo 'To Run Xvfb:          $ Xvfb :99 -ac -screen 0 1024x768x8&'
echo 'export DISPLAY:       $ export DISPLAY=:99'

echo 'then download driver from:  http://code.google.com/p/chromedriver/downloads/list'
echo 'unzip and copy the file to /usr/bin/'
