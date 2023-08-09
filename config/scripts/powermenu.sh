#!/bin/bash

opt=`eww get power-option`

if [[ $opt == "1" ]]; then
# swaylock -S --clock --effect-pixelate 64 
  swaylock -S --clock --effect-blur 12x12 # --indicator-y-position 810
elif [[ $opt == "2" ]]; then
  eww update power-option=1
  pkill Hyprland
elif [[ $opt == "3" ]]; then
  eww update power-option=1
  reboot
elif [[ $opt == "4" ]]; then
  eww update power-option=1
  shutdown -f now
else
  notify-send "Powermenu has encountered a problem!"
  eww update power-option=1
fi
