#!/bin/bash

sleep 3 # avoid database being unavailable

(
    ./manage.py compilescss &
    ./manage.py collectstatic --no-input &
    ./manage.py migrate --no-input
) || exit 1
