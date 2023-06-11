#!/bin/bash

lvlalt=`pamixer --get-volume-human | awk -F'%' '{ print $1 }'`
zero="0%"
mute="muted"

get-vol() {
  lvl=`pamixer --get-volume-human`
  if [ "$lvl" == "$zero" ]; then
    echo " "
  elif [ "$lvl" == "$mute" ]; then
    echo " "
  else
    echo " "
  fi
}

while [[ true ]]; do
  get-vol
  sleep 0.1
done
