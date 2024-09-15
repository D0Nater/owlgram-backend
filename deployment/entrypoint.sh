#!/bin/sh
set -e

if [ "$MODE" = "app" ]; then
  statusmgr run -p $PORT -h $HOST
elif [ "$MODE" = "dev" ]; then
  statusmgr dev --docker
elif [ "$MODE" = "shell" ]; then
  $@
else
  echo "ERROR: \$MODE is not set to \"app\", \"dev\" or \"shell\"."
  exit 1
fi
