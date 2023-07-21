#!/bin/bash

workspaces() {
  a=`hyprctl monitors | awk 'FNR == 7 { print $3 }'`
  o=`hyprctl workspaces | awk '{ print $3 }' | egrep -o '[0-9]+'`
  
  w1=bar-ws
  w2=bar-ws
  w3=bar-ws
  w4=bar-ws
  w5=bar-ws
  w6=bar-ws
  w7=bar-ws
  w8=bar-ws
  w9=bar-ws
  w10=bar-ws

  for i in $o
  do
    eval "w$i=bar-occupied-ws";
  done

  if [[ $a -eq 1 ]]; then
    w1=bar-active-ws
  elif [[ $a -eq 2 ]]; then
    w2=bar-active-ws
  elif [[ $a -eq 3 ]]; then
    w3=bar-active-ws
  elif [[ $a -eq 4 ]]; then
    w4=bar-active-ws
  elif [[ $a -eq 5 ]]; then
    w5=bar-active-ws
  elif [[ $a -eq 6 ]]; then
    w6=bar-active-ws
  elif [[ $a -eq 7 ]]; then
    w7=bar-active-ws
  elif [[ $a -eq 8 ]]; then
    w8=bar-active-ws
  elif [[ $a -eq 9 ]]; then
    w9=bar-active-ws
  elif [[ $a -eq 10 ]]; then
    w10=bar-active-ws
  fi

  echo "(box :class \"bar-workspace\" :orientation \"h\" :spacing 10 :space-evenly false :halign \"start\" :hexpand false (label :class \"$w1\" :text \"一\") (label :class \"$w2\" :text \"二\") (label :class \"$w3\" :text \"三\") (label :class \"$w4\" :text \"四\") (label :class \"$w5\" :text \"五\") (label :class \"$w6\" :text \"六\") (label :class \"$w7\" :text \"七\") (label :class \"$w8\" :text \"八\") (label :class \"$w9\" :text \"九\") (label :class \"$w10\" :text \"十\"))"
}

workspaces
socat -U - UNIX-CONNECT:/tmp/hypr/$HYPRLAND_INSTANCE_SIGNATURE/.socket2.sock | while read -r _ ; do
  workspaces
done
