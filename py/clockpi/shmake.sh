#!/bin/bash

# Args:
#	1: host
#	2: command (stop, start, benchmark, etc)

function get_status {
	ssh "$1" "/usr/sbin/service clockpi status &>/dev/null"
	return $?
}

if [[ $2 == 'start' ]]; then
	get_status $1
	if [[ $? -ne 0 ]]; then
		ssh -t $1 "sudo /usr/sbin/service clockpi start"
	fi
fi

if [[ $2 == 'restart' ]]; then
	ssh -t $1 "sudo /usr/sbin/service clockpi restart"
fi

if [[ $2 == 'stop' ]]; then
	get_status $1
	if [[ $? -ne 3 ]]; then
		ssh -t $1 "sudo /usr/sbin/service clockpi stop"
	fi
fi

