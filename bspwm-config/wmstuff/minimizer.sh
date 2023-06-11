#!/bin/bash
MIN=minimize
UN=unminimize
activewin=$(xdotool getactivewindow)
if [ "$1" == "$MIN" ]; then
  echo $activewin >> ~/test/minimizer/window-cache.txt
  xdotool windowunmap $(xdotool getactivewindow)
  echo "minimizing..."
elif [ "$1" == "$UN" ]; then
  lastwin=`awk 'END{ print }' ~/test/minimizer/window-cache.txt`
  xdotool windowmap $lastwin
  sed -i '$d' ~/test/minimizer/window-cache.txt
  echo "restoring..."
fi
