#!/bin/sh

SUCCESS=0

for i in `seq 1 10`; do
    flask db upgrade &> /dev/null
    if [ $? -eq 0 ]; then
        SUCCESS=1
        break
    fi
    s=`expr $i \* 3`
    echo "INFO: Try $i failed. Going to sleep for $s seconds..."
    sleep $s
done

if [ $SUCCESS -eq 0 ]; then
    echo "ERROR: Could not connect to database."
    exit 1
fi

coverage run

coverage html

coverage xml
