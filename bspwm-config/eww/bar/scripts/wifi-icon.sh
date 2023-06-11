#!/bin/bash
strength=`iwconfig wlan0 | grep "Link Quality=" | awk -F'=' '{ print $2 }' | awk -F'/' '{ print $1 }'`

strength-icon() {
  if [[ $strength -le 14 ]]; then
    echo "󰤯 "
  elif [[ $strength -le 28 ]]; then 
    echo "󰤟 "
  elif [[ $strength -le 42 ]]; then
    echo "󰤢 "
  elif [[ $strength -le 56 ]]; then
    echo "󰤥 "
  elif [[ $strength -le 70 ]]; then
    echo "󰤨 "
  fi
}

strength-icon
