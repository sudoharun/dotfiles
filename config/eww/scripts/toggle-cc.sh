#!/bin/bash

TOGGLE=~/.toggle

if [ ! -e $TOGGLE ]; then
  touch ~/.toggle
  eww -c ~/.config/eww/control-center open back
else
  rm ~/.toggle
  eww -c ~/.config/eww/control-center close-all
fi
