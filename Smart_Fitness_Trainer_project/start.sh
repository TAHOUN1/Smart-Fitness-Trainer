#!/bin/sh
exec uvicorn backend:app --host 0.0.0.0 --port $PORT 