#!/bin/bash

# *** VARIABLES ***
CURRENT_IMAGE=1
# wait time between captures in seconds
WAIT_TIME=5

# *** READ ARGUMENTS ***
while [ $# -gt 1 ] ; do
	case $1 in
	-t )		WAIT_TIME=$2
			shift
			;;
	default )	;;
	esac
	shift
done

# ***** MAIN PROGRAM ******

# make sure necessary directories exist
mkdir -p /home/pi/pics/

while [ 1 ] ; do
	while [ -f "/home/pi/pics/image_${CURRENT_IMAGE}.jpg" ] ; do
		CURRENT_IMAGE=$((CURRENT_IMAGE+1))
	done

	#echo "Wait time is ${WAIT_TIME} seconds"
	EXPOSURE_TIME=$((WAIT_TIME * 1000 / 2))
	#echo "Exposure Time: ${EXPOSURE_TIME}"
	raspistill --nopreview -w 1080 -h 720 -t "${EXPOSURE_TIME}" -o "/home/pi/pics/image_${CURRENT_IMAGE}.jpg"
	sleep ${WAIT_TIME}
done
