#!/bin/bash

if [[ $1 == "inc" ]]; then
  pamixer -i 5
elif [[ $1 == "dec" ]]; then
  pamixer -d 5
elif [[ $1 == "mute" ]]; then
  pamixer -t
elif [[ $1 == "mic" ]]; then
  pamixer --default-source -t
fi
