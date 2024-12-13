#!/bin/bash

while [[ $(astal -l | grep "network" | wc -l) < 1 ]]; do
    sleep 0.5
    python network/app.py &
done
