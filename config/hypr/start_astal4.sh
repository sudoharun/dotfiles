#!/bin/bash

while [[ $(astal -l | grep "gtk4" | wc -l) < 1 ]]; do
  sleep 0.25
  python $HOME/.config/astal/app.py &
done
