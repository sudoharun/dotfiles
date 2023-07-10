#!/bin/bash

aw=`hyprctl monitors | grep active | awk '{print "Workspace " $3}'`
ow1=`hyprctl workspaces | grep "workspace ID 1" | awk -F"ID" '{ print $2 }' | awk -F"(" '{ print $1 }'`
ow2=`hyprctl workspaces | grep "workspace ID 2" | awk -F"ID" '{ print $2 }' | awk -F"(" '{ print $1 }'`
ow3=`hyprctl workspaces | grep "workspace ID 3" | awk -F"ID" '{ print $2 }' | awk -F"(" '{ print $1 }'`
ow4=`hyprctl workspaces | grep "workspace ID 4" | awk -F"ID" '{ print $2 }' | awk -F"(" '{ print $1 }'`
ow5=`hyprctl workspaces | grep "workspace ID 5" | awk -F"ID" '{ print $2 }' | awk -F"(" '{ print $1 }'`
ow6=`hyprctl workspaces | grep "workspace ID 6" | awk -F"ID" '{ print $2 }' | awk -F"(" '{ print $1 }'`
ow7=`hyprctl workspaces | grep "workspace ID 7" | awk -F"ID" '{ print $2 }' | awk -F"(" '{ print $1 }'`
ow8=`hyprctl workspaces | grep "workspace ID 8" | awk -F"ID" '{ print $2 }' | awk -F"(" '{ print $1 }'`
ow9=`hyprctl workspaces | grep "workspace ID 9" | awk -F"ID" '{ print $2 }' | awk -F"(" '{ print $1 }'`
ow10=`hyprctl workspaces | grep "workspace ID 10" | awk -F"ID" '{ print $2 }' | awk -F"(" '{ print $1 }'`

w1() {
  if [[ $aw == "Workspace 1" ]]; then
    echo bar-active-ws
  elif [[ $ow1 -eq 1 ]]; then
    echo bar-occupied-ws
  else
    echo bar-ws
  fi
}

w2() {
  if [[ $aw == "Workspace 2" ]]; then
    echo bar-active-ws
  elif [[ $ow2 -eq 2 ]]; then
    echo bar-occupied-ws
  else
    echo bar-ws
  fi
}

w3() {
  if [[ $aw == "Workspace 3" ]]; then
    echo bar-active-ws
  elif [[ $ow3 -eq 3 ]]; then
    echo bar-occupied-ws
  else
    echo bar-ws
  fi
}

w4() {
  if [[ $aw == "Workspace 4" ]]; then
    echo bar-active-ws
  elif [[ $ow4 -eq 4 ]]; then
    echo bar-occupied-ws
  else
    echo bar-ws
  fi
}

w5() {
  if [[ $aw == "Workspace 5" ]]; then
    echo bar-active-ws
  elif [[ $ow5 -eq 5 ]]; then
    echo bar-occupied-ws
  else
    echo bar-ws
  fi
}

w6() {
  if [[ $aw == "Workspace 6" ]]; then
    echo bar-active-ws
  elif [[ $ow6 -eq 6 ]]; then
    echo bar-occupied-ws
  else
    echo bar-ws
  fi
}

w7() {
  if [[ $aw == "Workspace 7" ]]; then
    echo bar-active-ws
  elif [[ $ow7 -eq 7 ]]; then
    echo bar-occupied-ws
  else
    echo bar-ws
  fi
}

w8() {
  if [[ $aw == "Workspace 8" ]]; then
    echo bar-active-ws
  elif [[ $ow8 -eq 8 ]]; then
    echo bar-occupied-ws
  else
    echo bar-ws
  fi
}

w9() {
  if [[ $aw == "Workspace 9" ]]; then
    echo bar-active-ws
  elif [[ $ow9 -eq 9 ]]; then
    echo bar-occupied-ws
  else
    echo bar-ws
  fi
}

w10() {
  if [[ $aw == "Workspace 10" ]]; then
    echo bar-active-ws
  elif [[ $ow10 -eq 10 ]]; then
    echo bar-occupied-ws
  else
    echo bar-ws
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
elif [[ $1 == w6 ]]; then
  w6
elif [[ $1 == w7 ]]; then
  w7
elif [[ $1 == w8 ]]; then
  w8
elif [[ $1 == w9 ]]; then
  w9
elif [[ $1 == w10 ]]; then
  w10
fi
