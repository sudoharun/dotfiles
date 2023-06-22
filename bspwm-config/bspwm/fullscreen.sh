#!/bin/bash
bspc subscribe node_state | while read -r _ _ _ _ state flag; do
  if [ "$state" != "fullscreen" ]; then
    continue
  fi

  if [ "$flag" == on ]; then
    eww -c ~/.config/eww/bar close-all
    killall eww
    killall picom
  else
    xrandr --output eDP1 --auto
    eww daemon
    eww -c ~/.config/eww/bar open bar
    picom &
  fi
done &
