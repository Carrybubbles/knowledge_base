#!/bin/sh

while ! nc -z h2o 54321; do
  sleep 0.1
done

echo "h2o started"

exec "$@"
