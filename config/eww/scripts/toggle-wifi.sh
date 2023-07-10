#!/bin/bash

TOGGLEWIFI=~/.toggle-wifi

if [ ! -e $TOGGLEWIFI ]; then
  touch ~/.toggle-wifi
  iwctl station wlan0 disconnect vodafone7D0B7A
else
  rm ~/.toggle-wifi
  iwctl station wlan0 connect vodafone7D0B7A
fi
