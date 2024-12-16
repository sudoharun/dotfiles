#!/bin/bash

while [[ $(astal -l | grep "osd" | wc -l) < 1 ]]; do
    sleep 0.5
    python osds/app.py &
done
