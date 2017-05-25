#!/bin/bash

### BEGIN INIT INFO
# Provides:		start_captureimage.sh
# Required-Start:	$remote_fs $syslog
# Required-Stop:	$remote_fs $syslog
# Default-Start:	2 3 4 5
# Default-Stop:		0 1 6
# Short-Description:	Start the script on boot
# Description:		Enable the time lapsification of greatness
### END INIT INFO

# in order to remove this script from the startup routine, modify
# the file /etc/rc.local. Remove the line containing the script
# execution.

# *** functions ***
function start {
	touch /home/pi/pics/status.log
	# defaults to 5 second rate
	/home/pi/pics/captureimage.sh -t 5 & > /home/pi/pics/status.log
}	# end start

function stop {
	# just stop the service
	killall -9 captureimage.sh
}	# end stop

function status {
	cat /home/pi/pics/status.log
}	# end status

# *** main logic ***
case "$1" in
	start )
		start
		;;
	stop )
		stop
		;;
	status )
		echo "might be running"
		;;
	* )
		echo "invalid command"
		exit 1
		;;
esac

exit 0
