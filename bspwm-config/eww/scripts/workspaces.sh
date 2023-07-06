#!/bin/bash

aw=`wmctrl -d | grep "*" | awk '{ print $9 }'`
occ1=`bspc query -D -d .occupied --names | grep -i '1'`
occ2=`bspc query -D -d .occupied --names | grep -i '2'`
occ3=`bspc query -D -d .occupied --names | grep -i '3'`
occ4=`bspc query -D -d .occupied --names | grep -i '4'`
occ5=`bspc query -D -d .occupied --names | grep -i '5'`

w1() {
  if [[ $aw -eq 1 ]]; then
    echo active-ws
  elif [[ $occ1 -eq 1 ]]; then
    echo occupied-ws
  else
    echo ws
  fi
}

w2() {
  if [[ $aw -eq 2 ]]; then
    echo active-ws
  elif [[ $occ2 -eq 2 ]]; then
    echo occupied-ws
  else
    echo ws
  fi
}

w3() {
  if [[ $aw -eq 3 ]]; then
    echo active-ws
  elif [[ $occ3 -eq 3 ]]; then
    echo occupied-ws
  else
    echo ws
  fi
}

w4() {
  if [[ $aw -eq 4 ]]; then
    echo active-ws
  elif [[ $occ4 -eq 4 ]]; then
    echo occupied-ws
  else
    echo ws
  fi
}

w5() {
  if [[ $aw -eq 5 ]]; then
    echo active-ws
  elif [[ $occ5 -eq 5 ]]; then
    echo occupied-ws
  else
    echo ws
  fi
}

if [[ $1 == w1 ]]; then
  w1
elif [[ $1 == w2 ]]; then
  w2
elif [[ $1 == w3 ]]; then
  w3
elif [[ $1 == w4 ]]; then
  w4
elif [[ $1 == w5 ]]; then
  w5
fi
