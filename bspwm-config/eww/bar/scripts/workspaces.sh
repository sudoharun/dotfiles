#!/bin/bash
workspace() {
  aw=`wmctrl -d | grep "*" | awk '{ print $9 }'`

  if [[ $aw -eq 1 ]]; then
    echo -e "(box :class \"workspaces\" :orientation \"h\" :spacing \"10\" :space-evenly false :halign \"start\" (label :class \"active-ws\" :text \"一\") (label :class \"ws\" :text \"二\") (label :class \"ws\" :text \"三\") (label :class \"ws\" :text \"四\") (label :class \"ws\" :text \"五\"))"
  elif [[ $aw -eq 2 ]]; then
    echo -e "(box :class \"workspaces\" :orientation \"h\" :spacing \"10\" :space-evenly false :halign \"start\" (label :class \"ws\" :text \"一\") (label :class \"active-ws\" :text \"二\") (label :class \"ws\" :text \"三\") (label :class \"ws\" :text \"四\") (label :class \"ws\" :text \"五\"))"
  elif [[ $aw -eq 3 ]]; then
    echo -e "(box :class \"workspaces\" :orientation \"h\" :spacing \"10\" :space-evenly false :halign \"start\" (label :class \"ws\" :text \"一\") (label :class \"ws\" :text \"二\") (label :class \"active-ws\" :text \"三\") (label :class \"ws\" :text \"四\") (label :class \"ws\" :text \"五\"))"
  elif [[ $aw -eq 4 ]]; then
    echo -e "(box :class \"workspaces\" :orientation \"h\" :spacing \"10\" :space-evenly false :halign \"start\" (label :class \"ws\" :text \"一\") (label :class \"ws\" :text \"二\") (label :class \"ws\" :text \"三\") (label :class \"active-ws\" :text \"四\") (label :class \"ws\" :text \"五\"))"
  elif [[ $aw -eq 5 ]]; then
    echo -e "(box :class \"workspaces\" :orientation \"h\" :spacing \"10\" :space-evenly false :halign \"start\" (label :class \"ws\" :text \"一\") (label :class \"ws\" :text \"二\") (label :class \"ws\" :text \"三\") (label :class \"ws\" :text \"四\") (label :class \"active-ws\" :text \"五\"))"
  fi
}

while [[ true ]]; do
  workspace
  sleep 0.1
done
