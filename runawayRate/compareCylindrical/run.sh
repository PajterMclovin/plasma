#!/bin/sh
# Created by Peter Halldestam 19/8/21.
#
# run.sh: combines configurations from a python script (GENERATE_SETTINGS) and
#         runs DREAM simulations for each created DREAM setting.
#

DREAM_PATH="/home/peterhalldestam/DREAM/" # /path/to/DREAM/
DREAMI_PATH="${DREAM_PATH}build/iface/dreami"
DREAM_SETTINGS_DIR="./dream_settings/"
DREAM_OUTPUTS_DIR="./outputs/"
GENERATE_SETTINGS="generateElectricScan.py" # "generateTemperatureScan.py"

## create new dream_settings files OR use old OR quit
mkdir -p $DREAM_SETTINGS_DIR
if test -z "$(ls $DREAM_SETTINGS_DIR)"
then
    echo "No old dream_settings files detected."
    echo "Creating new dream_settings files from $GENERATE_SETTINGS."
    python3 $GENERATE_SETTINGS
else
    echo "Old dream_settings files detected!"
    while true
    do
        read -p "Do you wish to replace them? (y/n/quit)" ans
        case $ans in
            [Yy]* )
                echo "Deleting old dream_settings files and create new from $GENERATE_SETTINGS."
                rm $DREAM_SETTINGS_DIR*
                python3 $GENERATE_SETTINGS
                break;;
            [Nn]* )
                echo "Using old dream_settings files."
                break;;
            quit )
                exit;;
            * )
                echo "Please answer y/n/quit.";;
        esac
    done
fi
echo ""

## remove old output files
mkdir -p $DREAM_OUTPUTS_DIR
if test -z "$(ls $DREAM_OUTPUTS_DIR)"
then
    echo "No old output files detected."
else
    echo "Old output files detected!"
    while true
    do
        read -p "Do you wish to delete them? (y/n)" ans
        case $ans in
            [Yy]* )
                echo "Deleting old output files."
                rm $DREAM_OUTPUTS_DIR*
                break;;
            [Nn]* | quit )
                exit;;
            * )
                echo "Please answer y/n/quit.";;
        esac
    done
fi
echo ""

## run DREAM simulations
echo "Run DREAM using $DREAMI_PATH."
for settings_file in $DREAM_SETTINGS_DIR*.h5
do
    /.$DREAMI_PATH $settings_file
done
