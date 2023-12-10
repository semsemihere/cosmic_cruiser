#!/bin/bash
# Some common shell stuff.

echo "Importing from common.sh"

DB=ccDB
USER=semihong
CONNECT_STR="mongodb+srv://semihong:asdf1234@cosmiccrusier.3cyi8m1.mongodb.net/"


# dynamically detect project directory so we don't have t manually put it every time
PROJECT_DIR=$(dirname "$(realpath "$0")")

# set data directory using project directory
DATA_DIR="$PROJECT_DIR"

# set the backup directory using data directory -- bkup folder
BKUP_DIR="$DATA_DIR/bkup"


# if [ -z "$DATA_DIR" ]; then
#     DATA_DIR="/Users/nishm/Programming/cosmic_cruiser/data"
# fi
# BKUP_DIR="$DATA_DIR/bkup"

EXP=/usr/bin/mongoexport
IMP=/usr/bin/mongoimport

if [ -z $MONGODB_PASSWORD ]
then
    echo "You must set MONGODB_PASSWORD in your env before running this script."
    exit 1
fi

declare -a GameCollections=("categories" "ems" "nutrition" "test_collect" "users")
