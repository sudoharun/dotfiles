#!/bin/bash
name() {
  winame=`xdotool getactivewindow getwindowname`

  # Uncommment for character limit
  # And change line 12 variable name
  # windowname=`echo ${winame::150}`
  
  if [[ $winame == "" ]]; then
    echo "Desktop"
  else
    echo "$winame"
  fi
}
name
