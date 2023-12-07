#!/bin/sh
# Some common shell stuff.

echo "Importing from common.sh"

DB=ccDB
USER=semihong
CONNECT_STR="mongodb+srv://koukoumongo1.yud9b.mongodb.net/"
if [ -z $DATA_DIR ]
then
    DATA_DIR=/Users/chris/cosmic/cosmic_cruiser/data
    
fi
BKUP_DIR=$DATA_DIR/bkup
EXP=/usr/local/bin/mongoexport
IMP=/usr/local/bin/mongoimport

if [ -z $MONGODB_PASSWORD ]
then
    echo "You must set MONGODB_PASSWORD in your env before running this script."
    exit 1
fi

declare -a CategoryCollections=("categories" "ems" "nutrition" "test_collect" "users")