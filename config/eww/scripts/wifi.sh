#!/bin/bash

strength=`iwconfig wlan0 | grep "Link Quality=" | awk -F'=' '{ print $2 }' | awk -F'/' '{ print $1 }'`

wf=`echo "$strength*100/70" | bc`

icon() {
  if [[ $strength -eq 0 ]]; then
    echo 󰤭 
  elif [[ $strength -le 14 ]]; then
    echo 󰤯 
  elif [[ $strength -le 28 ]]; then 
    echo 󰤟 
  elif [[ $strength -le 42 ]]; then
    echo 󰤢 
  elif [[ $strength -le 56 ]]; then
    echo 󰤥 
  elif [[ $strength -le 70 ]]; then
    echo 󰤨 
  else
    echo 󰤭 
  fi
}

percentage() {
  echo "$wf%"
}

if [[ $1 == icon ]]; then
  icon
elif [[ $1 == percentage ]]; then
  percentage
fi
