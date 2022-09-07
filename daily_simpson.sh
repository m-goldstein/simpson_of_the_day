#!/bin/bash -e
OLD_PWD=`pwd`
HOME_DIR=/home/mg/simpson_of_the_day
WWW=$HOME_DIR/www
INDEX_HTML=index.html
HTML_DIR=/var/www/`uname -n`/public_html/
cd $HOME_DIR
python3 bot.py --today
cp $WWW/$INDEX_HTML $HTML_DIR/$INDEX_HTML
cd $OLD_PWD
