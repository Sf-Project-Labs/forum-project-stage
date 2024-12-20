#!/bin/sh
# wait-for-it.sh: Wait for a service to be ready

host=$1
shift
port=$1
shift
cmd="$@"

while ! nc -z $host $port; do
  echo "Waiting for $host:$port to be ready..."
  sleep 2
done

exec $cmd
