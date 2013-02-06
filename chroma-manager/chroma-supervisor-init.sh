#!/bin/bash
#
# chroma-supervisor     Runs supervisord with the Chroma configuration file
#
# chkconfig: 345 88 12
# description: Runs supervisord with the Chroma configuration file
# processname: supervisord

. /etc/init.d/functions

export SERVICE_NAME=chroma-supervisor
export PROJECT_PATH=/usr/share/chroma-manager
export PID_FILE=/var/run/chroma-supervisor.pid
export LOG_DIR=/var/log/chroma
export PYTHONPATH=${PROJECT_PATH}
export SUPERVISOR_CONFIG=${PROJECT_PATH}/production_supervisord.conf


start() {
    action "Starting ${SERVICE_NAME}" supervisord --pidfile=${PID_FILE} -c ${SUPERVISOR_CONFIG} -d ${PROJECT_PATH} -l ${LOG_DIR}/supervisord.log
    echo
}

stop() {
    # Use -TERM to prevent killproc -KILL'ing supervisord when it doesn't
    # exit immediately: that would orphan supervisor's children.
    action "Stopping ${SERVICE_NAME}: " killproc -p ${PID_FILE} ${SERVICE_NAME} -TERM
    echo
}

case "$1" in
    start)
        start
        exit $?
        ;;
    stop)
        stop
        exit $?
        ;;
    status)
        status -p ${PID_FILE} ${SERVICE_NAME}
        exit $?
        ;;

    restart|force-reload)
        stop
        start
        exit $?
        ;;
  *)
        echo "Usage: $0 {start|stop|restart|status|force-reload}" >&2
        exit 1
        ;;
esac

exit 0

