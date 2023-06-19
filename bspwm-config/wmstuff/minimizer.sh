#!/bin/bash
MIN=minimize
UN=unminimize
activewin=$(xdotool getactivewindow)
if [ "$1" == "$MIN" ]; then
  echo $activewin >> ~/.config/wmstuff/window-cache.txt
  xdotool windowunmap $(xdotool getactivewindow)
  echo "minimizing..."
elif [ "$1" == "$UN" ]; then
  lastwin=`awk 'END{ print }' ~/.config/wmstuff/window-cache.txt`
  xdotool windowmap $lastwin
  sed -i '$d' ~/.config/wmstuff/window-cache.txt
  echo "restoring..."
fi
