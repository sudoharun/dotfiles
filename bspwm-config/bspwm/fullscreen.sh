#!/bin/bash

EWW=$HOME/.eww/target/release/eww

bspc subscribe node_state | while read -r _ _ _ _ state flag; do
  if [ "$state" != "fullscreen" ]; then
    continue
  fi

  if [ "$flag" == on ]; then
    $EWW -c ~/.config/eww/bar close-all
    killall $EWW
    killall picom
  else
    xrandr --output eDP1 --auto
    $EWW daemon
    $EWW -c ~/.config/eww/bar open bar
    picom &
  fi
done &
