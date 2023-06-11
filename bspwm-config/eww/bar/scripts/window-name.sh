#!/bin/bash
name() {
  winame=`xdotool getactivewindow getwindowname`
  windowname=`echo ${winame::150}`
  echo -e "(box :class \"window-name\" :orientation \"h\" :halign \"center\" (label :text \"$windowname\"))"
}

while [[ true ]]; do
  name
  sleep 0.1
done
