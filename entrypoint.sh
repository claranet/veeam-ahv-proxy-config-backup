#!/bin/sh

ARGS=""

test -n "${PROXY_HOSTNAME}" && ARGS="${ARGS} --proxy-hostname '${PROXY_HOSTNAME}'"
test -n "${PROXY_USERNAME}" && ARGS="${ARGS} --proxy-username '${PROXY_USERNAME}'"
test -n "${PROXY_PASSWORD}" && ARGS="${ARGS} --proxy-password '${PROXY_PASSWORD}'"
test -n "${BACKUP_PASSWORD}" && ARGS="${ARGS} --backup-password '${BACKUP_PASSWORD}'"
test -n "${OUT_DIR}" && ARGS="${ARGS} --out-dir '${OUT_DIR}'"

eval "/usr/local/bin/python /usr/src/app/backup.py ${ARGS} $@"
