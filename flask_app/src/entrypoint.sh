#!/bin/sh

set -u

echo "Waiting for DB..."
#while ! nc -z $HOST $PORT; do
while ! nc -z postgres 5432; do
  sleep 2
done

echo "DB started"

exec "$@"

