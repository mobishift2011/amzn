#!/bin/bash
source /usr/local/bin/virtualenvwrapper.sh
mkvirtualenv djCatalog
workon djCatalog
pip install -r requirements.txt