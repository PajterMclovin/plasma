#!/bin/sh
# Created by Peter Halldestam 19/8/21.
#
# clear.sh: Removes all dream_settings and output files.
#
#

DREAM_SETTINGS_DIR="./dream_settings/"
DREAM_OUTPUTS_DIR="./outputs/"

## make sure cwd is script dir
cd "${0%/*}"

## check if empty and confirm removal
if test -z "$(ls $DREAM_SETTINGS_DIR)" || test -z "$(ls $DREAM_OUTPUTS_DIR)"
then
    echo "No old files detected."
else
    echo "Old files detected!"
    while true
    do
        read -p "Do you wish to delete them? (y/n)" ans
        case $ans in
            [Yy]* )
                rm -v $DREAM_SETTINGS_DIR*
                rm -v $DREAM_OUTPUTS_DIR*
                exit;;
            [Nn]* )
                echo "Ok bye..."
                exit;;
            quit )
                exit;;
            * )
                echo "Please answer y/n.";;
        esac
    done
fi
