#!/bin/bash -e
ARCHIVE_DIR=archive
BIOPICS_DIR=biopics
ASSETS_DIR=assets
WWW_DIR=www
SEEN=seen

mkdir -p $ARCHIVE_DIR/{1..12}/{1..31}
mkdir -p $BIOPICS_DIR
mkdir -p $ASSETS_DIR
mkdir -p $WWW_DIR
cp $ASSETS_DIR/$SEEN $ASSETS_DIR/$SEEN.bak
python3 -m pip install requests,bs4

