#!/bin/bash
name() {
  winame=`xdotool getactivewindow getwindowname`
  # windowname=`echo ${winame::150}`
  if [[ $winame == "" ]]; then
    echo "Desktop"
  else
    echo "$winame"
  fi
}
name
