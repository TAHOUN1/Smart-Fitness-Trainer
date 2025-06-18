#!/bin/sh
echo "DEBUG: Script started"
echo "PORT is: $PORT"
env
if [ -z "$PORT" ]; then
  echo "ERROR: PORT is not set!"
  exit 1
fi
exec uvicorn backend:app --host 0.0.0.0 --port $PORT 