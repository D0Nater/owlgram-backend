#!/bin/sh
set -e

if [ "$MODE" = "app" ]; then
  owlgram run -p $PORT -h $HOST
elif [ "$MODE" = "dev" ]; then
  owlgram dev --docker
elif [ "$MODE" = "migrations" ]; then
  pwstorage db migrate
elif [ "$MODE" = "shell" ]; then
  $@
else
  echo "ERROR: \$MODE is not set to \"app\", \"dev\", \"migrations\" or \"shell\"."
  exit 1
fi
