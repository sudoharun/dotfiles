#!/bin/bash
name() {
  winame=`hyprctl activewindow | grep "title" | awk -F":" '{ print $2 }'`
  windowname=`echo ${winame::125}`
  if [[ $winame == "" ]]; then
    echo "Desktop"
  else
    echo "$windowname"
  fi
}
name
