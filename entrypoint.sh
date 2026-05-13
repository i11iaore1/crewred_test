#!/bin/sh

set -e

echo "Starting uvicorn..."
exec uvicorn app.main:app --host 0.0.0.0 $@