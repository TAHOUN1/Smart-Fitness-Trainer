#!/bin/sh
echo "PORT is: $PORT"
env
exec uvicorn backend:app --host 0.0.0.0 --port $PORT 